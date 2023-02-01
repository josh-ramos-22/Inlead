## Inlead - Database Object
##
## Josh Ramos (josh-ramos-22)
## January 2023
##
## Python object that connects to the database
## Wrapper for psycopg2

import psycopg2

class Database:
    # def __init__(self):
    #     self.conn = psycopg2.connect("dbname=inlead")
    #     self.cur = self.conn.cursor()
        
    # def get_cursor(self):
    #     return self.cur
    
    # Need to create a new connection for each thread, in order
    # to prevent recursive connection entries
    def get_conn(self):
        return psycopg2.connect("dbname=inlead")
    
    
global database

database = Database()