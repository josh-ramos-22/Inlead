import pytest
import requests
import json
from src import config

from tests.helpers import user_dict, register_user1, register_user2, clear

####################################### TESTS FOR AUTH_REGISTER ####################################

def test_simple(clear):
    resp = requests.post(config.url + 'auth/register/v1',
                            json = user_dict("josh@josh.com", "password", "joshthejosh"))
    
    assert resp.status_code == 200

def test_duplicate_username(clear):
    resp = requests.post(config.url + 'auth/register/v1',
                            json = user_dict("josh2@josh.com", "password", "joshthejosh"))
    
    assert resp.status_code == 200
    
    resp = requests.post(config.url + 'auth/register/v1',
                            json = user_dict("josh23@josh.com", "password", "joshthejosh"))
    
    assert resp.status_code == 400


def test_duplicate_email(clear):
    resp = requests.post(config.url + 'auth/register/v1',
                            json = user_dict("josh2@josh.com", "password", "joshTHEjosh"))
    
    assert resp.status_code == 200
    
    resp = requests.post(config.url + 'auth/register/v1',
                            json = user_dict("josh2@josh.com", "password", "otherjosh"))
    
    assert resp.status_code == 400
    
####################################### TESTS FOR AUTH_LOGIN ####################################
def test_simple_login(clear, register_user1):
    expected_user_id = register_user1['auth_user_id']
    
    resp = requests.post(config.url + 'auth/login/v1', 
                            json = { 'email' : 'email@email.com', 'password' : 'joshiscool'})
    
    assert resp.status_code == 200
    assert json.loads(resp.text)['auth_user_id'] == expected_user_id
    
    # Try basic task such as creating a competition
    
    request_body = {
        'token' : json.loads(resp.text)['token'],
        'name'  : "Mahjong World Cup 2023",
        'max_points_per_log' : 15,
        'description' : "Winner takes all!",
        'is_points_moderated' : True
    }
    
    resp2 = requests.post(config.url + 'competition/create/v1',
                            json = request_body)
    
    assert resp2.status_code == 200


def test_login_fails_after_failed_registration(clear, register_user1):
    resp = requests.post(config.url + 'auth/register/v1',
                            json = user_dict("fakejosh@josh.com", "password", "joshthejosh"))
    
    assert resp.status_code == 400
    
    ## Login should now fail for fake josh since the username 'joshthejosh' has already been taken
    
    resp2 = requests.post(config.url + 'auth/login/v1', 
                            json = { 'email' : 'fakejosh@josh.com', 'password' : 'password'})
    
    assert resp2.status_code == 400
    

def test_login_with_wrong_password(clear, register_user1):
    resp2 = requests.post(config.url + 'auth/login/v1', 
                            json = { 'email' : 'email@email.com', 'password' : 'ThisAinttherightPWLOLOLOL'})
    
    assert resp2.status_code == 400

def test_login_password_case_sensitivity(clear, register_user1):
    resp2 = requests.post(config.url + 'auth/login/v1', 
                            json = { 'email' : 'email@email.com', 'password' : 'JosHISCoOL'})
    
    assert resp2.status_code == 400

def test_login_with_invalid_email(clear, register_user1):
    resp2 = requests.post(config.url + 'auth/login/v1', 
                            json = { 'email' : 'unregistered@email.com', 'password' : 'Thisshouldntwork'})
    
    assert resp2.status_code == 400
    
####################################### TESTS FOR AUTH_LOGOUT ####################################

def test_works_after_register(clear, register_user1):
    token = register_user1['token']
    resp = requests.post(config.url +'auth/logout/v1', json = {"token": token})
    
    assert resp.status_code == 200
    
    # Try basic task such as creating a competition, making sure it fails
    
    request_body = {
        'token' : token,
        'name'  : "Mahjong World Cup 2023",
        'max_points_per_log' : 15,
        'description' : "Winner takes all!",
        'is_points_moderated' : True
    }
    
    resp2 = requests.post(config.url + 'competition/create/v1',
                            json = request_body)
    
    assert resp2.status_code == 403
    
    
def test_double_logout_fails(clear, register_user1):
    token = register_user1['token']
    resp = requests.post(config.url +'auth/logout/v1', json = {"token": token})
    
    assert resp.status_code == 200
    
    token = register_user1['token']
    resp = requests.post(config.url +'auth/logout/v1', json = {"token": token})
    
    assert resp.status_code == 403