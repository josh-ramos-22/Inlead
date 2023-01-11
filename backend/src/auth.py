## Inlead - Authorisation and Authentication Functions
##
## Josh Ramos (josh-ramos-22)
## January 2023
##

from src import auth_helpers, sec
import hashlib
from src.error import InputError, AccessError
from src.db import database

'''
Register a new user

Parameters
- email - The email of the user
- password - the user's selected password
- username - the username of the new user

Returns
- token - the session token of the user
- auth_user_id - the user's assigned user id.
'''
def register(email, password, username):
    
    email = email.lower()
    
    # check if email is in use
    if auth_helpers.is_email_in_use(email):
        raise InputError("Email already in use")
    
    # Check if username is in use
    if auth_helpers.is_username_in_use(username):
        raise InputError("Username already in use") 
    
    auth_user_id = None
    
    # Create user, inserting them into the database
    with database.get_conn() as conn:
        with conn.cursor() as cur:
            qry = """
                INSERT into Players(handle_str, email, password)
                            VALUES(%s, %s, %s)
                RETURNING id
                ;
            """
            qry_params = [username, email, hashlib.sha256(password.encode()).hexdigest()]
            
            cur.execute(qry, qry_params)
            auth_user_id = cur.fetchone()[0]
            
            conn.commit()
            
    
    # Generate a session token inserting it to the database
    
    token = sec.generate_jwt(auth_user_id)
    
    return {
        'token' : token,
        'auth_user_id' : auth_user_id
    }


'''
Log in an existing user user

Parameters
- email - The email of the user
- password - the user's password

Returns
- token - the session token of the user
- auth_user_id - the user's assigned user id.
'''
def login(email, password):
    email = email.lower()
    with database.get_conn() as conn:
        with conn.cursor() as cur:
            qry = """
                SELECT id, password
                FROM   Players
                WHERE  email = %s
            """
            qry_params = [email]
            
            cur.execute(qry, qry_params)
            qry_result = cur.fetchone()
            
            if not qry_result:
                raise InputError("We could not verify an account with those credentials.")
            
            auth_user_id, stored_password = qry_result
            
            if (hashlib.sha256(password.encode()).hexdigest() != stored_password):
                raise InputError("We could not verify an account with those credentials.")
            
    token = sec.generate_jwt(auth_user_id)
    
    return {
        'token' : token,
        'auth_user_id' : auth_user_id
    }

def logout(token):
    if not sec.is_valid_token(token):
        raise AccessError("Invalid Session Token")
    
    with database.get_conn() as conn:
        with conn.cursor() as cur:
            qry = "DELETE from Tokens WHERE Token = %s"
            qry_params = (token,)
            cur.execute(qry, qry_params)
            
            conn.commit()
            
            return {}