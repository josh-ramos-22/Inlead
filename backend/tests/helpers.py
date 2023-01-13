## Helpers for Inlead tests
##
## By Josh Ramos January 2023
##

import pytest
from src import config
import json
import requests

# Returns a user_dict containing the parameters of 'auth/register/v1'
def user_dict(email, password, username):
    return {
        'email': email,
        'password': password,
        'username' : username
    }

# Register a Sample user
@pytest.fixture
def register_user1():
    resp1 = requests.post(config.url + 'auth/register/v1', 
                            json = user_dict("email@email.com", "joshiscool", "joshthejosh"))
    return json.loads(resp1.text)

# Register a second sample user
@pytest.fixture
def register_user2():
    resp2 = requests.post(config.url + 'auth/register/v1', 
                            json = user_dict("cino@cino.com", "cinoiscool", "cinothedog"))
    return json.loads(resp2.text)

@pytest.fixture
def clear():
    requests.delete(config.url + 'clear/v1')
    
@pytest.fixture
def sample_comp1(register_user1):
    token = register_user1['token']
    
    request_body = {
        'token' : token,
        'name'  : "Sample Competition",
        'max_points_per_log' : 15,
        'description' : "Winner takes all!",
        'is_points_moderated' : True
    }
    
    resp = requests.post(config.url + 'competition/create/v1', json = request_body)
    
    ret = json.loads(resp.text)
    print(ret)
    
    return {'owner_tok': token, 'owner_id': register_user1['auth_user_id'], 'comp_id': ret['comp_id']}

@pytest.fixture
def comp_with_30_players(sample_comp1):
    token = sample_comp1['owner_tok']
    comp_id = sample_comp1['comp_id']
    
    # Create and add 29 users to the comp
    for i in range(29):
        resp1 = requests.post(config.url + 'auth/register/v1', 
                        json = user_dict(f"emai{i}l@email.com", "password", f"sample{i}"))
        assert resp1.status_code == 200
        
        sample_tok = json.loads(resp1.text)['token']
        
        resp2 = requests.post(config.url + 'competition/join/v1',
                        json = { 'token' : sample_tok, 'comp_id' : comp_id})
        assert resp2.status_code == 200

    return {'owner_tok': token, 'owner_id': sample_comp1['owner_id'], 'comp_id': comp_id}