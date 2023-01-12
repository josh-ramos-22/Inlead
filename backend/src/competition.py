## Inlead - Competition Functions
##
## Josh Ramos (josh-ramos-22)
## January 2023
##

from src import sec
from src.db import database
import datetime

'''
Given a valid token, create a channel

@pre: all input is validated

Parameters
- auth_user_id - the id of the player trying to create the channel
- name - the name of the channel
- max_points_per_log, the maximum number of points one can log after a game
- description - optional description of the competition
- is_points_moderated - boolean which is true if points must get approval before contributing to the leaderboard

Returns
- comp_id - the id of the newly created competition.

'''
@sec.authorise
def create(auth_user_id, name, max_points_per_log, description, is_points_moderated):
    with database.get_conn() as conn:
        with conn.cursor() as cur:
            # Create Channel Record
            qry = """
                INSERT INTO Competitions(name, description, is_active, start_time, num_games, creator, is_points_moderated, max_points_per_log)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
                ;
            """
            qry_params = [name, description, False, datetime.datetime.now().isoformat(), 0, auth_user_id, is_points_moderated, max_points_per_log]
            cur.execute(qry, qry_params)
            comp_id = cur.fetchone()[0]
            
            # Add user to channel as a moderator
            qry2 = """
                INSERT INTO CompetitionParticipants(player, competition, is_moderator, score)
                VALUES (%s, %s, %s, %s)
                ;
            """
            qry2_params = [auth_user_id, comp_id, True, 0]
            cur.execute(qry2, qry2_params)

            conn.commit()

            return {
                'comp_id' : comp_id
            }

'''
Return a list of all the competitions the user is a part of

Parameters
    - auth_user_id - the id of the user accessing their list
    
Returns
    - a list of dictionaries of shape {comp_id, name, is_active}
'''
@sec.authorise
def list(auth_user_id):
    with database.get_conn() as conn:
        with conn.cursor() as cur:
            qry = """
                SELECT c.id, c.name, c.is_active
                FROM   Competitions c
                JOIN   CompetitionParticipants cp ON (cp.competition = c.id)
                WHERE  cp.player = %s
            """
            
            cur.execute(qry, (auth_user_id,))

            return {
                'competitions' : [  {
                    'comp_id'   : comp_id,
                    'name'      : name,
                    'is_active' : is_active
                    } for comp_id, name, is_active in cur.fetchall()
                ]
            }

