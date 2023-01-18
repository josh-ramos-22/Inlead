## Tests for Inlead Point endpoints

from tests.helpers import user_dict, register_user1, register_user2, clear, sample_comp1, comp_with_30_players, moderated_comp1
import pytest
from src import config
import json
import requests

################################### TESTS FOR POINTS_LOG ##################################

def test_points_appear_instantly_in_unmoderated_leaderboard(clear, sample_comp1, register_user2):
    # join as user 2, log 2 points, check leaderboard has user 2 on top with 2 points
    token = register_user2['token']
    u_id  = register_user2['auth_user_id']
    comp_id = sample_comp1['comp_id']
    
    resp1 = requests.post(config.url + 'competition/join/v1',
                        json = { 'token' : token, 'comp_id' : comp_id})
    assert resp1.status_code == 200
    
    resp2 = requests.post(config.url + 'points/log',
                        json = { 'token' : token, 'comp_id' : comp_id, 'points' : 2 })
    assert resp2.status_code == 200
    ret2 = json.loads(resp2.text)
    assert ret2['request_id'] == -1
    
    resp3 = requests.get(config.url + 'competition/leaderboard/v1',
                            params = { 'token': token, 'comp_id' : comp_id, 'start' : 0 } )
    assert resp3.status_code == 200
    
    ret = json.loads(resp3.text)
    leaderboard = ret['leaderboard']
    leader = leaderboard[0]
    assert leader['u_id'] == u_id
    assert leader['score'] == 2
    assert leader['is_moderator'] == False

def test_points_do_not_appear_instantly_in_moderated_leaderboard(clear, moderated_comp1, register_user2):
    token = register_user2['token']
    u_id  = register_user2['auth_user_id']
    comp_id = moderated_comp1['comp_id']
    
    resp1 = requests.post(config.url + 'competition/join/v1',
                        json = { 'token' : token, 'comp_id' : comp_id})
    assert resp1.status_code == 200
    
    resp2 = requests.post(config.url + 'points/log',
                        json = { 'token' : token, 'comp_id' : comp_id, 'points' : 2 })
    assert resp2.status_code == 200
    ret2 = json.loads(resp2.text)
    assert ret2['request_id'] != -1
    
    resp3 = requests.get(config.url + 'competition/leaderboard/v1',
                            params = { 'token': token, 'comp_id' : comp_id, 'start' : 0 } )
    assert resp3.status_code == 200
    
    ret = json.loads(resp3.text)
    leaderboard = ret['leaderboard']
    # NO points should be logged yet
    for player in leaderboard:
        assert player['score'] == 0

def test_points_by_moderator_bypass_requests(clear, moderated_comp1):
    token = moderated_comp1['owner_tok']
    u_id  = moderated_comp1['owner_id']
    comp_id = moderated_comp1['comp_id']
    
    resp1 = requests.post(config.url + 'competition/join/v1',
                        json = { 'token' : token, 'comp_id' : comp_id})
    assert resp1.status_code == 200
    
    resp2 = requests.post(config.url + 'points/log',
                        json = { 'token' : token, 'comp_id' : comp_id, 'points' : 2 })
    assert resp2.status_code == 200
    ret2 = json.loads(resp2.text)
    assert ret2['request_id'] == -1
    
    resp3 = requests.get(config.url + 'competition/leaderboard/v1',
                            params = { 'token': token, 'comp_id' : comp_id, 'start' : 0 } )
    assert resp3.status_code == 200
    
    ret = json.loads(resp3.text)
    leaderboard = ret['leaderboard']
    leader = leaderboard[0]
    assert leader['u_id'] == u_id
    assert leader['score'] == 2
    assert leader['is_moderator'] == True