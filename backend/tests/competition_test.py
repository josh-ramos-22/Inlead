## Tests for Inlead Competition endpoints

from tests.helpers import user_dict, register_user1, register_user2, clear, sample_comp1
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