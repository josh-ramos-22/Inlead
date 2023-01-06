## Inlead - Flask Server
##
## Josh Ramos (josh-ramos-22)
## January 2023
##
## Backend server for Inlead\
## Some code reused from 2021 implementation of 'UNSW Streams'

import sys
import signal
import time

import json
from flask import Flask, request, send_from_directory
from flask_cors import CORS

from src import config

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

########################################################################################
###                              HTTP ENDPOINTS                                     ####
########################################################################################

### Authorisation endpoints

@APP.route("auth/register/v1", methods=['POST'])
def auth_register():
    pass

@APP.route("/auth/login/v1", methods=['POST'])
def auth_login():
    pass

@APP.route("/auth/logout/v1", methods=['POST'])
def auth_logout():
    pass




if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully) # For coverage
    APP.run(port=config.port) # Do not edit this port
