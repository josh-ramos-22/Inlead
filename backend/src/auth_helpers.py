## Inlead - Authorisation and Authentication Helper Functions
##
## Josh Ramos (josh-ramos-22)
## January 2023
##

from src.db import database

## Given an email, check if it's already in use.
def is_email_in_use(email):
    with database.get_conn() as db:
        with db.cursor() as cur:
            qry = "select email from players where email = %s;"
            
            qry_params = [email]
            
            cur.execute(qry, qry_params)
            
            return cur.fetchone() is not None    


## Given an username, check if it's already in use.
def is_username_in_use(username):
    with database.get_conn() as db:
        with db.cursor() as cur:
            qry = "select username from players where username = %s;"
            
            qry_params = [username]
            
            cur.execute(qry, qry_params)
            
            return cur.fetchone() is not None    