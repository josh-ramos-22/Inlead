## Tests for Inlead Competition endpoints

from tests.helpers import user_dict, register_user1, register_user2, clear, sample_comp1
import pytest
from src import config
import json
import requests

####################################### TESTS FOR CHANNEL_LIST ####################################

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