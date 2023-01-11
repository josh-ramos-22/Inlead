## Inlead - Misc Functions
## Josh Ramos (josh-ramos-22)
## January 2023
##
## Backend server for Inlead\
## Some code reused from 2021 implementation of 'UNSW Streams'

from src.db import database

def clear():
    with database.get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("TRUNCATE CompetitionParticipants, Competitions, Players, PointsRequests, Tokens CASCADE;")
        conn.commit()
        return {}
        