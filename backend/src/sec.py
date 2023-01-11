## Inlead - Security Functions
##
## Josh Ramos (josh-ramos-22)
## January 2023
##
## Code re-used from 2021 Assignment "UNSW Streams"

import uuid
import time
import jwt
from db import database

from error import AccessError

SECRET = "##M4J0nGIzC0OOL!"

'''
Generate a random ID using uuid

Arguments:
    none
Exceptions:
    None

Return Value:
    a randomly generated uuid
'''
def generate_id():
    return uuid.uuid4().int % int(time.time())


'''
Generate and store a JWT

Arguments:
    auth_user_id - the id of the user that is being authenticated
    
REturn Value:
    A newly generated JWT
'''
def generate_jwt(auth_user_id):
    session_id = generate_id()
    new_jwt = jwt.encode({'u_id' : auth_user_id, 'session_id': session_id}, SECRET, algorithm = 'HS256')
    
    # store token in database
    with database.get_conn() as conn:
        with conn.cursor as cur:
            qry = "INSERT into Tokens(token) VALUES (%s)"
            cur.execute(qry, (new_jwt,))
            conn.commit()

    return new_jwt


'''
Given a JSON Web Token, decrypt it and return it

Arguments:
    token - JWT token
    ...

Exceptions:
    none

Return Value:
    Returns the decrypted data stored in the JWT
'''
def decode_jwt(token):

    return jwt.decode(token, SECRET, algorithms = ['HS256'])


'''
Given a session token, return the user_id associated with that token

Arguments:
    token - string - Token of the user´s session
    ...

Exceptions:
    InputError - When token is invalid - not associated with any active session

Return Value:
    Returns u_id
'''
def get_u_id(token):

    ## TODO Check that the token exists / is active
    # if (token not in store['session_tokens']):
    #     raise AccessError(description = "Error: Invalid token")
    
    with database.get_conn() as conn:
        with conn.cursor() as cur:
            qry = """"
                select token from Tokens where token = %s
            """
            
            qry_params = [token]
            
            cur.execute(qry, qry_params)
            
            if cur.fetchone() is not None:
                raise AccessError("Invalid Token")

    decoded_tok = decode_jwt(token)

    return decoded_tok['u_id']


'''
Given a session token, return the session_id associated with that token

Arguments:
    token - string - Token of the user´s session
    ...

Exceptions:
    None

Return Value:
    Returns session_id
'''
def get_session_id(token):
    decoded_tok = decode_jwt(token)

    return decoded_tok['session_id']