## Inlead - Authorisation and Authentication Functions
##
## Josh Ramos (josh-ramos-22)
## January 2023
##

import auth_helpers
import sec 
import hashlib
from error import InputError, AccessError
from db import database

## Register a new user
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
            """
            qry_params = [username, email, hashlib.sha256(password.encode()).hexdigest()]
            
            cur.execute(qry, qry_params)
            auth_user_id = cur.fetchone()[0]
            
            conn.commit()
            
    
    # Generate a session token inserting it to the database
    
    token = sec.generate_jwt()
    
    return {
        'token' : token,
        'auth_user_id' : auth_user_id
    }

def login(db):
    pass

def logout(db):
    pass