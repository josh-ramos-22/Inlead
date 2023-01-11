## Inlead - Flask Server
##
## Josh Ramos (josh-ramos-22)
## January 2023
##
## Backend server for Inlead\
## Some code reused from 2021 implementation of 'UNSW Streams'

import sys
import psycopg2
import signal
import time

import json
from flask import Flask, request, send_from_directory
from flask_cors import CORS

from src import config, auth, other

def quit_gracefully(*args):
    exit(0)

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = json.dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__, static_folder = '../static/', static_url_path='/static/')
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

global conn
conn = None

########################################################################################
###                              HTTP ENDPOINTS                                     ####
########################################################################################

### Authorisation endpoints

@APP.route("/auth/register/v1", methods=['POST'])
def auth_register():
    data = request.get_json()
    ret = auth.register(data['email'], data['password'], data['username'])
    
    return json.dumps(ret)

@APP.route("/auth/login/v1", methods=['POST'])
def auth_login():
    data = request.get_json()
    ret = auth.login(data['email'], data['password'])
    
    return json.dumps(ret)

@APP.route("/auth/logout/v1", methods=['POST'])
def auth_logout():
    data = request.get_json()
    ret = auth.logout(data['token'])
    
    return json.dumps(ret)

### Competition endpoints

@APP.route("/competition/create/v1", methods=['POST'])
def competition_create():
    return {}
    
@APP.route("/competition/list/v1", methods=['GET'])
def competition_list():
    return {}
    
@APP.route("/competition/details/v1", methods=['GET'])
def competition_details():
    return {}

@APP.route("/competition/leaderboard/v1", methods=['GET'])
def competition_leaderboard():
    return {}

@APP.route("/competition/join/v1", methods=['POST'])
def competition_join():
    return {}

@APP.route("/competition/end/v1", methods=['POST'])
def competition_end():
    return {}

### Helper Endpoints

@APP.route("/clear/v1", methods=['DELETE'])
def clear():
    ret = other.clear()
    return json.dumps(ret)



if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully)
    APP.run(port=config.port)