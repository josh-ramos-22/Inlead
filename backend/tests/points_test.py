## Tests for Inlead Point endpoints

from tests.helpers import user_dict, register_user1, register_user2, register_user3, clear, sample_comp1, comp_with_30_players, moderated_comp1
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
    
    resp2 = requests.post(config.url + 'points/log/v1',
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
    
def test_cant_log_points_into_finished_comp(clear, sample_comp1, register_user2):
    owner_tok = sample_comp1['owner_tok']
    comp_id = sample_comp1['comp_id']
    player_tok = register_user2['token']
    
    # End the competition
    resp = requests.post(config.url + 'competition/end/v1',
                        json = { 'token' : owner_tok, 'comp_id' : comp_id})
    assert resp.status_code == 200
    
    # Try to log points: should fail
    resp2 = requests.post(config.url + 'points/log/v1',
                        json = { 'token' : player_tok, 'comp_id' : comp_id, 'points' : 2 })
    assert resp2.status_code == 400

def test_points_do_not_appear_instantly_in_moderated_leaderboard(clear, moderated_comp1, register_user2):
    token = register_user2['token']
    u_id  = register_user2['auth_user_id']
    comp_id = moderated_comp1['comp_id']
    
    resp1 = requests.post(config.url + 'competition/join/v1',
                        json = { 'token' : token, 'comp_id' : comp_id})
    assert resp1.status_code == 200
    
    resp2 = requests.post(config.url + 'points/log/v1',
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
    
    resp2 = requests.post(config.url + 'points/log/v1',
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
    

################################### TESTS FOR POINTS_APPROVE ##################################
def test_approve_works(clear, moderated_comp1, register_user2):
    token = register_user2['token']
    owner_tok = moderated_comp1['owner_tok']
    
    u_id  = register_user2['auth_user_id']
    comp_id = moderated_comp1['comp_id']
    
    resp1 = requests.post(config.url + 'competition/join/v1',
                        json = { 'token' : token, 'comp_id' : comp_id})
    assert resp1.status_code == 200
    
    resp2 = requests.post(config.url + 'points/log/v1',
                        json = { 'token' : token, 'comp_id' : comp_id, 'points' : 2 })
    assert resp2.status_code == 200
    ret2 = json.loads(resp2.text)

    request_id = ret2['request_id']
    print(request_id)
    assert request_id != -1
    
    ## Approve the request
    resp3 = requests.post(config.url + 'points/approve/v1',
                        json = { 'token' : owner_tok, 'request_id' : request_id } )
    assert resp3.status_code == 200

    
    resp4 = requests.get(config.url + 'competition/leaderboard/v1',
                            params = { 'token': token, 'comp_id' : comp_id, 'start' : 0 } )
    assert resp4.status_code == 200
    
    ret = json.loads(resp4.text)
    leaderboard = ret['leaderboard']
    leader = leaderboard[0]
    assert leader['u_id'] == u_id
    assert leader['score'] == 2
    assert leader['is_moderator'] == False

def test_non_mod_cant_approve(clear, moderated_comp1, register_user2, register_user3):
    token = register_user2['token']
    not_owner_tok = register_user3['token']
    
    u_id  = register_user2['auth_user_id']
    comp_id = moderated_comp1['comp_id']
    
    resp0 = requests.post(config.url + 'competition/join/v1',
                        json = { 'token' : token, 'comp_id' : comp_id})
    assert resp0.status_code == 200
    
    resp1 = requests.post(config.url + 'competition/join/v1',
                        json = { 'token' : not_owner_tok, 'comp_id' : comp_id})
    assert resp1.status_code == 200
    
    resp2 = requests.post(config.url + 'points/log/v1',
                        json = { 'token' : token, 'comp_id' : comp_id, 'points' : 2 })
    assert resp2.status_code == 200
    ret2 = json.loads(resp2.text)

    request_id = ret2['request_id']
    assert request_id != -1
    
    ## Try to approve the request
    resp3 = requests.post(config.url + 'points/approve/v1',
                        json = { 'token' : not_owner_tok, 'request_id' : request_id } )
    assert resp3.status_code == 403


def test_approve_invalid_request(clear, moderated_comp1):
    owner_tok = moderated_comp1['owner_tok']
    
    resp3 = requests.post(config.url + 'points/approve/v1',
                        json = { 'token' : owner_tok, 'request_id' : -12312 } )
    assert resp3.status_code == 400


################################### TESTS FOR POINTS_REJECT ##################################
def test_reject_works(clear, moderated_comp1, register_user2):
    token = register_user2['token']
    owner_tok = moderated_comp1['owner_tok']
    
    u_id  = register_user2['auth_user_id']
    comp_id = moderated_comp1['comp_id']
    
    resp1 = requests.post(config.url + 'competition/join/v1',
                        json = { 'token' : token, 'comp_id' : comp_id})
    assert resp1.status_code == 200
    
    resp2 = requests.post(config.url + 'points/log/v1',
                        json = { 'token' : token, 'comp_id' : comp_id, 'points' : 2 })
    assert resp2.status_code == 200
    ret2 = json.loads(resp2.text)

    request_id = ret2['request_id']
    assert request_id != -1
    
    ## Reject
    resp3 = requests.post(config.url + 'points/reject/v1',
                        json = { 'token' : owner_tok, 'request_id' : request_id } )
    assert resp3.status_code == 200
    
    resp3 = requests.get(config.url + 'competition/leaderboard/v1',
                            params = { 'token': token, 'comp_id' : comp_id, 'start' : 0 } )
    assert resp3.status_code == 200
    
    ret = json.loads(resp3.text)
    leaderboard = ret['leaderboard']
    # No points should be logged
    for player in leaderboard:
        assert player['score'] == 0

def test_non_mod_cant_reject(clear, moderated_comp1, register_user2, register_user3):
    token = register_user2['token']
    not_owner_tok = register_user3['token']
    
    u_id  = register_user2['auth_user_id']
    comp_id = moderated_comp1['comp_id']
    
    resp0 = requests.post(config.url + 'competition/join/v1',
                        json = { 'token' : token, 'comp_id' : comp_id})
    assert resp0.status_code == 200
    
    resp1 = requests.post(config.url + 'competition/join/v1',
                        json = { 'token' : not_owner_tok, 'comp_id' : comp_id})
    assert resp1.status_code == 200
    
    resp2 = requests.post(config.url + 'points/log/v1',
                        json = { 'token' : token, 'comp_id' : comp_id, 'points' : 2 })
    assert resp2.status_code == 200
    ret2 = json.loads(resp2.text)

    request_id = ret2['request_id']
    assert request_id != -1
    
    ## Try to reject the request
    resp3 = requests.post(config.url + 'points/reject/v1',
                        json = { 'token' : not_owner_tok, 'request_id' : request_id } )
    assert resp3.status_code == 403

def test_reject_invalid_request(clear, moderated_comp1):
    owner_tok = moderated_comp1['owner_tok']
    
    resp3 = requests.post(config.url + 'points/reject/v1',
                        json = { 'token' : owner_tok, 'request_id' : -12312 } )
    assert resp3.status_code == 400

################################### TESTS FOR POINTS_OVERRIDE ##################################

def test_override_works(clear, moderated_comp1, register_user2):
    token = register_user2['token']
    owner_tok = moderated_comp1['owner_tok']
    
    u_id  = register_user2['auth_user_id']
    comp_id = moderated_comp1['comp_id']
    
    resp1 = requests.post(config.url + 'competition/join/v1',
                        json = { 'token' : token, 'comp_id' : comp_id})
    assert resp1.status_code == 200
    
    resp2 = requests.post(config.url + 'points/override/v1',
                        json = { 'token' : owner_tok, 'u_id' : u_id, 'comp_id' : comp_id, 'new_points' : 231 })
    assert resp2.status_code == 200
    
    resp3 = requests.get(config.url + 'competition/leaderboard/v1',
                            params = { 'token': token, 'comp_id' : comp_id, 'start' : 0 } )
    assert resp3.status_code == 200
    
    ret = json.loads(resp3.text)
    leaderboard = ret['leaderboard']
    leader = leaderboard[0]
    assert leader['u_id'] == u_id
    assert leader['score'] == 231
    assert leader['is_moderator'] == False

def test_non_mod_cant_override_points(clear, moderated_comp1, register_user2):
    token = register_user2['token']
    owner_tok = moderated_comp1['owner_tok']
    
    u_id  = register_user2['auth_user_id']
    comp_id = moderated_comp1['comp_id']
    
    resp1 = requests.post(config.url + 'competition/join/v1',
                        json = { 'token' : token, 'comp_id' : comp_id})
    assert resp1.status_code == 200
    
    resp2 = requests.post(config.url + 'points/override/v1',
                        json = { 'token' : owner_tok, 'u_id' : u_id, 'comp_id' : comp_id, 'new_points' : 231 })
    assert resp2.status_code == 403

def test_override_invalid_input(clear, moderated_comp1, register_user2, register_user3):
    member_tok = register_user2['token']
    owner_tok = moderated_comp1['owner_tok']
    non_member_tok = register_user3['token']
    
    member_id  = register_user2['auth_user_id']
    non_member_id = register_user3['auth_user_id']
    comp_id = moderated_comp1['comp_id']
    
    resp1 = requests.post(config.url + 'competition/join/v1',
                        json = { 'token' : member_tok, 'comp_id' : comp_id})
    assert resp1.status_code == 200
    
    # Try overriding points in a non exisitant compeition
    resp2 = requests.post(config.url + 'points/override/v1',
                        json = { 'token' : owner_tok, 'u_id' : member_id, 'comp_id' : -234, 'new_points' : 231 })
    assert resp2.status_code == 400
    
    # Try overriding the points of a player not in the competition
    resp2 = requests.post(config.url + 'points/override/v1',
                        json = { 'token' : owner_tok, 'u_id' : non_member_id, 'comp_id' : comp_id, 'new_points' : 231 })
    assert resp2.status_code == 400
    

################################### TESTS FOR POINTS_REQUEST_LIST ##################################
def test_requests_appear_in_list(clear, moderated_comp1, register_user2, regsiter_user3):
    token = register_user2['token']
    owner_tok = moderated_comp1['owner_tok']
    
    u_id  = register_user2['auth_user_id']
    comp_id = moderated_comp1['comp_id']
    
    resp1 = requests.post(config.url + 'competition/join/v1',
                        json = { 'token' : token, 'comp_id' : comp_id})
    assert resp1.status_code == 200
    
    for _ in range(3):
        resp2 = requests.post(config.url + 'points/log/v1',
                            json = { 'token' : token, 'comp_id' : comp_id, 'points' : 2 })
        assert resp2.status_code == 200
        ret2 = json.loads(resp2.text)

        request_id = ret2['request_id']
        assert request_id != -1
        
    resp3 = requests.get(config.url + 'points/request_list/v1',
                        params = {'token' : owner_tok, 'comp_id' : comp_id})
    assert resp3.status_code == 200
    
    req_list = json.loads(resp3.text)['requests']
    
    assert len(req_list) == 3

def test_non_mod_cant_access_requests(clear, moderated_comp1, register_user2):
    token = register_user2['token']
    owner_tok = moderated_comp1['owner_tok']
    
    u_id  = register_user2['auth_user_id']
    comp_id = moderated_comp1['comp_id']
    
    resp1 = requests.post(config.url + 'competition/join/v1',
                        json = { 'token' : token, 'comp_id' : comp_id})
    assert resp1.status_code == 200
    

    resp3 = requests.get(config.url + 'points/request_list/v1',
                        params = {'token' : token, 'comp_id' : comp_id})
    assert resp3.status_code == 403

def test_list_empty_after_game_is_ended(clear, moderated_comp1, register_user2):
    token = register_user2['token']
    owner_tok = moderated_comp1['owner_tok']
    
    u_id  = register_user2['auth_user_id']
    comp_id = moderated_comp1['comp_id']
    
    resp1 = requests.post(config.url + 'competition/join/v1',
                        json = { 'token' : token, 'comp_id' : comp_id})
    assert resp1.status_code == 200
    
    for _ in range(3):
        resp2 = requests.post(config.url + 'points/log/v1',
                            json = { 'token' : token, 'comp_id' : comp_id, 'points' : 2 })
        assert resp2.status_code == 200
        ret2 = json.loads(resp2.text)

        request_id = ret2['request_id']
        assert request_id != -1
        
    # BEfore getting the request list, end the game.
    resp3 = requests.post(config.url + 'competition/end/v1',
                        json = { 'token' : owner_tok, 'comp_id' : comp_id })
    assert resp3.status_code == 200
    
    # Request list should be empty now    
    resp4 = requests.get(config.url + 'points/request_list/v1',
                        params = {'token' : owner_tok, 'comp_id' : comp_id})
    assert resp4.status_code == 200
    
    req_list = json.loads(resp4.text)['requests']
    assert len(req_list) == 0