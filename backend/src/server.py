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

from src import config, auth, other, competition, points

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
    data = request.get_json()
    ret = competition.create(data['token'], data['name'], data['max_points_per_log'], data['description'], data['is_points_moderated'])
    
    return json.dumps(ret)
    
@APP.route("/competitions/list/v1", methods=['GET'])
def competition_list():
    token = request.args.get('token')
    ret = competition.list(token)
    
    return json.dumps(ret)
    
@APP.route("/competition/details/v1", methods=['GET'])
def competition_details():
    token = request.args.get('token')
    comp_id = int(request.args.get('comp_id'))
    
    ret = competition.details(token, comp_id)
    
    return json.dumps(ret)

@APP.route("/competition/join/v1", methods=['POST'])
def competition_join():
    data = request.get_json()
    ret = competition.join(data['token'], data['comp_id'])
    
    return json.dumps(ret)

@APP.route("/competition/leaderboard/v1", methods=['GET'])
def competition_leaderboard():
    token = request.args.get('token')
    comp_id = int(request.args.get('comp_id'))
    start = int(request.args.get('start'))
    
    ret = competition.leaderboard(token, comp_id, start)
    
    return json.dumps(ret)


@APP.route("/competition/end/v1", methods=['POST'])
def competition_end():
    data = request.get_json()
    ret = competition.end(data['token'], data['comp_id'])
    
    return json.dumps(ret)


### Points Endpoints
@APP.route("/points/log/v1", methods=['POST'])
def points_log():
    data = request.get_json()
    ret = points.log(data['token'], data['comp_id'], data['points'])
    
    return json.dumps(ret)

@APP.route("/points/approve/v1", methods=['POST'])
def points_approve():
    data = request.get_json()
    ret = points.approve(data['token'], data['request_id'])
    
    return json.dumps(ret)

@APP.route("/points/reject/v1", methods=['POST'])
def points_reject():
    data = request.get_json()
    ret = points.reject(data['token'], data['request_id'])
    
    return json.dumps(ret)

### Helper Endpoints

@APP.route("/clear/v1", methods=['DELETE'])
def clear():
    ret = other.clear()
    return json.dumps(ret)



if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully)
    APP.run(port=config.port)