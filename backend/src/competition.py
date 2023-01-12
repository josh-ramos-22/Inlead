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
            qry = """
                INSERT INTO Competitions(comp_name, description, is_complete, start_time, num_games, creator, is_points_moderated, max_points_per_log)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
                ;
            """
            
            qry_params = [name, description, False, datetime.datetime.now().isoformat(), 0, auth_user_id, is_points_moderated, max_points_per_log]
            
            cur.execute(qry, qry_params)
            comp_id = cur.fetchone()[0]
            
            conn.commit()
            
            return {
                'comp_id' : comp_id
            }
            