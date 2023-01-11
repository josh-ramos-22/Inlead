import pytest
import requests
import json
from src import config

@pytest.fixture
def clear():
    requests.delete(config.url + 'clear/v1')

################################################ HELPER FUNCTIONS ####################################

# Returns a user_dict containing the parameters of 'auth/register/v1'
def user_dict(email, password, username):
    return {
        'email': email,
        'password': password,
        'username' : username
    }
    
@pytest.fixture
def register_user1():
    resp1 = requests.post(config.url + 'auth/register/v1', 
                            json = user_dict("email@email.com", "joshiscool", "joshthejosh"))
    return json.loads(resp1.text)

@pytest.fixture
def register_user2():
    resp2 = requests.post(config.url + 'auth/register/v1', 
                            json = user_dict("cino@cino.com", "cinoiscool", "cinothedog"))
    return json.loads(resp2.text)



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
    
    ## TODO: add test for basic request with invalid token.
    
    
def test_double_logout_fails(clear, register_user1):
    token = register_user1['token']
    resp = requests.post(config.url +'auth/logout/v1', json = {"token": token})
    
    assert resp.status_code == 200
    
    token = register_user1['token']
    resp = requests.post(config.url +'auth/logout/v1', json = {"token": token})
    
    assert resp.status_code == 403