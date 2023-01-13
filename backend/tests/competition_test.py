## Tests for Inlead Competition endpoints

from tests.helpers import user_dict, register_user1, register_user2, clear, sample_comp1, comp_with_30_players
import pytest
from src import config
import json
import requests

####################################### TESTS FOR COMP_LIST ####################################

def test_no_comps(clear, register_user1):
    token = register_user1['token']
    
    resp = requests.get(config.url + 'competitions/list/v1', params = { "token": token })
    competitions = json.loads(resp.text)['competitions']
    
    assert len(competitions) == 0

def test_own_comp_appears(clear, sample_comp1):
    token = sample_comp1['owner_tok']
    resp = requests.get(config.url + 'competitions/list/v1', params = { "token": token })
    competitions = json.loads(resp.text)['competitions']
    
    assert len(competitions) == 1
    
    for key in competitions[0]:
        assert key in ['name', 'comp_id', 'is_active']

def test_non_member_cant_see_comp(clear, sample_comp1, register_user2):
    token = register_user2['token']
    
    resp = requests.get(config.url + 'competitions/list/v1', params = { "token": token })
    competitions = json.loads(resp.text)['competitions']
    
    # as user 2 is not a member of the sample channel, it should not appear in their list
    assert len(competitions) == 0
    

####################################### TESTS FOR COMP_DETAILS ##################################
def test_all_details_correct(clear, sample_comp1):
    owner_tok = sample_comp1['owner_tok']
    owner_id = sample_comp1['owner_id']
    
    comp_id = sample_comp1['comp_id']
    
    resp = requests.get(config.url + 'competition/details/v1', params = { 'token' : owner_tok, 'comp_id': comp_id})
    assert resp.status_code == 200
    
    details = json.loads(resp.text)
    
    assert details['name'] == "Sample Competition"
    assert details['is_active'] == True
    assert details['owner'] == owner_id
    assert details['max_points_per_log'] == 15
    assert details['is_points_moderated'] == True

def test_invalid_channel_id(clear, register_user1):
    resp = requests.get(config.url + 'competition/details/v1', params = { 'token' : register_user1['token'], 'comp_id': -2312})
    assert resp.status_code == 400

def test_non_member_cant_access_details(clear, sample_comp1, register_user2):
    comp_id = sample_comp1['comp_id']
    intruder_tok = register_user2['token']
    
    resp = requests.get(config.url + 'competition/details/v1', params = { 'token' : intruder_tok, 'comp_id': comp_id})
    assert resp.status_code == 403
    

################################### TESTS FOR COMPETITION JOIN ##################################

def test_simple_join(clear, sample_comp1, register_user2):
    token = register_user2['token']
    comp_id = sample_comp1['comp_id']
    
    resp = requests.post(config.url + 'competition/join/v1',
                        json = { 'token' : token, 'comp_id' : comp_id})
    
    assert resp.status_code == 200

def test_double_join_fails(clear, sample_comp1):
    token = sample_comp1['owner_tok']
    comp_id = sample_comp1['comp_id']
    
    resp = requests.post(config.url + 'competition/join/v1',
                        json = { 'token' : token, 'comp_id' : comp_id})
    
    assert resp.status_code == 400

def test_join_invalid_comp(clear, register_user1):
    token = register_user1['token']
    comp_id = -23213
    
    resp = requests.post(config.url + 'competition/join/v1',
                        json = { 'token' : token, 'comp_id' : comp_id})
    
    assert resp.status_code == 400


################################### TESTS FOR COMPETITION END ##################################

def test_end_disables_joining(clear, sample_comp1, register_user2):
    owner_tok = sample_comp1['owner_tok']
    joiner_tok = register_user2['token']
    
    comp_id = sample_comp1['comp_id']
    
    # End the competition
    resp = requests.post(config.url + 'competition/end/v1',
                        json = { 'token' : owner_tok, 'comp_id' : comp_id})
    assert resp.status_code == 200
    
    # Try joining the ended competition as user 2; should fail.
    resp2 = requests.post(config.url + 'competition/join/v1',
                        json = { 'token' : joiner_tok, 'comp_id' : comp_id})
    
    assert resp2.status_code == 403

def test_non_mod_cant_end_competition(clear, sample_comp1, register_user2):
    joiner_tok = register_user2['token']
    
    comp_id = sample_comp1['comp_id']
    
    # Join the comp as user 2
    resp = requests.post(config.url + 'competition/join/v1',
                        json = { 'token' : joiner_tok, 'comp_id' : comp_id})
    assert resp.status_code == 200
    
    # attempt to end the comp as user 2\
    resp2 = requests.post(config.url + 'competition/end/v1',
                        json = { 'token' : joiner_tok, 'comp_id' : comp_id})
    assert resp2.status_code == 403
    
def test_non_member_cant_end_competition(clear, sample_comp1, register_user2):
    joiner_tok = register_user2['token']
    
    comp_id = sample_comp1['comp_id']
    
    # attempt to end the comp as user 2\
    resp2 = requests.post(config.url + 'competition/end/v1',
                        json = { 'token' : joiner_tok, 'comp_id' : comp_id})
    assert resp2.status_code == 403

def test_end_invalid_id(clear, register_user1):
    owner_tok = register_user1['token']
    comp_id = -23
    
    # End the competition
    resp = requests.post(config.url + 'competition/end/v1',
                        json = { 'token' : owner_tok, 'comp_id' : comp_id})
    assert resp.status_code == 400

def test_double_end_fails(clear, sample_comp1):
    owner_tok = sample_comp1['owner_tok']
    comp_id = sample_comp1['comp_id']
    
    # End the competition
    resp = requests.post(config.url + 'competition/end/v1',
                        json = { 'token' : owner_tok, 'comp_id' : comp_id})
    assert resp.status_code == 200
    
    # Try to end the competition again
    resp2 = requests.post(config.url + 'competition/end/v1',
                        json = { 'token' : owner_tok, 'comp_id' : comp_id})
    assert resp2.status_code == 400
    
## TODO Test that pending points requests are deleted for competitions that have been ended

################################### TESTS FOR COMPETITION LEADERBOARD ##################################

def test_leaderboard_one_participant(clear, sample_comp1):
    token = sample_comp1['owner_tok']
    comp_id = sample_comp1['comp_id']
    
    resp = requests.get(config.url + 'competition/leaderboard/v1',
                            params = { 'token': token, 'comp_id' : comp_id, 'start' : 0 } )
    assert resp.status_code == 200

    ret = json.loads(resp.text)
    
    leaderboard = ret['leaderboard']
    assert len(leaderboard) == 1
    assert ret['end'] == -1
    assert ret['start'] == 0

def test_leaderboard_first_10(clear, comp_with_30_players):
    token = comp_with_30_players['owner_tok']
    comp_id = comp_with_30_players['comp_id']
    
    resp = requests.get(config.url + 'competition/leaderboard/v1',
                            params = { 'token': token, 'comp_id' : comp_id, 'start' : 0 } )
    assert resp.status_code == 200

    ret = json.loads(resp.text)
    
    leaderboard = ret['leaderboard']
    assert len(leaderboard) == 10
    assert ret['end'] == 10
    assert ret['start'] == 0

def test_leaderboard_middle_10(clear, comp_with_30_players):
    token = comp_with_30_players['owner_tok']
    comp_id = comp_with_30_players['comp_id']
    
    resp = requests.get(config.url + 'competition/leaderboard/v1',
                            params = { 'token': token, 'comp_id' : comp_id, 'start' : 10 } )
    assert resp.status_code == 200

    ret = json.loads(resp.text)
    
    leaderboard = ret['leaderboard']
    assert len(leaderboard) == 10
    assert ret['end'] == 20
    assert ret['start'] == 10


def test_leaderboard_last_5(clear, comp_with_30_players):
    token = comp_with_30_players['owner_tok']
    comp_id = comp_with_30_players['comp_id']
    
    resp = requests.get(config.url + 'competition/leaderboard/v1',
                            params = { 'token': token, 'comp_id' : comp_id, 'start' : 25 } )
    assert resp.status_code == 200
    ret = json.loads(resp.text)
    
    leaderboard = ret['leaderboard']
    assert len(leaderboard) == 5
    assert ret['end'] == -1
    assert ret['start'] == 25


def test_leaderboard_invalid_start(clear, comp_with_30_players):
    token = comp_with_30_players['owner_tok']
    comp_id = comp_with_30_players['comp_id']
    
    resp = requests.get(config.url + 'competition/leaderboard/v1',
                            params = { 'token': token, 'comp_id' : comp_id, 'start' : 45 } )
    assert resp.status_code == 400