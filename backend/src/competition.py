## Inlead - Competition Functions
##
## Josh Ramos (josh-ramos-22)
## January 2023
##

from src import sec
from src.db import database
from src.error import InputError, AccessError
import datetime
import psycopg2

'''
Given a valid token, create a competition

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
                INSERT INTO Competitions(name, description, is_active, start_time, num_games, owner, is_points_moderated, max_points_per_log)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
                ;
            """
            qry_params = [name, description, True, datetime.datetime.now().isoformat(), 0, auth_user_id, is_points_moderated, max_points_per_log]
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
                ;
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

'''
Given a competition id, return basic details about the competition

Parameters
    - auth_user_id - the id of the user making the request
    - comp_id - the id of the competition
    
Exceptions
    - InputError - when the given Comp Id is invalid
    - AccessError - when the user is not a participant in the competition
'''
@sec.authorise
def details(auth_user_id, comp_id):
    with database.get_conn() as conn:
        with conn.cursor() as cur:
            qry = """
                SELECT c.id, c.name, c.is_active, c.owner, c.max_points_per_log, c.is_points_moderated
                FROM   Competitions c
                JOIN   CompetitionParticipants cp ON (c.id = cp.competition)
                WHERE  c.id = %s
                AND    cp.player = %s
            """
            
            cur.execute(qry, (comp_id, auth_user_id))
            
            result = cur.fetchone()
            
            if result is None:
                cur.execute("SELECT id FROM Competitions WHERE id = %s", (comp_id,))
                if cur.fetchone() is not None:
                    raise AccessError("You are not a participant in this Competition")
                
                raise InputError("Invalid Competition")
            
            comp_id, name, is_active, owner, max_points_per_log, is_points_moderated = result
            
            return {
                'comp_id'            : comp_id,
                'name'               : name,
                'is_active'          : is_active,
                'owner'              : owner,
                'max_points_per_log' : max_points_per_log,
                'is_points_moderated': is_points_moderated
            }

'''
Join a competition with the given comp_id

Parameters
    - auth_user_id - the id of the user wanting to join
    - comp_id - the competition id
    
Exceptions
    - InputError when
        - The user is already part of the competition
        - The comp_id is invalid
    - AccessError if the competition is inactive
    
Returns
    - None
'''
@sec.authorise
def join(auth_user_id, comp_id):
    with database.get_conn() as conn:
        with conn.cursor() as cur:
            qry = """
                SELECT is_active
                FROM   Competitions
                WHERE  id = %s
            """
            
            cur.execute(qry, (comp_id,))
            result = cur.fetchone()
            
            if result is None:
                raise InputError("Invalid Channel")
            elif not result[0]:
                raise AccessError("This competition has already ended")
            
            qry2 = """
                INSERT INTO CompetitionParticipants(player, competition, is_moderator, score)
                VALUES (%s, %s, %s, %s);
            """
            qry2_params = [auth_user_id, comp_id, False, 0]
            
            try:
                cur.execute(qry2, qry2_params)
            except psycopg2.errors.UniqueViolation as e:
                raise InputError("You are already participating in this competition")
            
            conn.commit()
            
            return {}

'''
End an active competition

Parameters
    - auth_user_id - the id of the user wanting to end the competition
    - comp_id - the competition id
    
Exceptions
    - InputError when
        - The competition is inactive
        - The comp_id is invalid
    - AccessError if the user attempting to end the competition is not a moderator
    
Returns
    - None
'''
@sec.authorise
def end(auth_user_id, comp_id):
    with database.get_conn() as conn:
        with conn.cursor() as cur:
            qry = """
                SELECT cp.is_moderator, c.is_active
                FROM   CompetitionParticipants cp
                JOIN   Competitions c on (c.id = cp.competition)
                WHERE  c.id = %s 
                AND    cp.player = %s
                ;
            """
            cur.execute(qry, (comp_id, auth_user_id) )
            result = cur.fetchone()
            
            if result is None:
                cur.execute("SELECT id FROM Competitions WHERE id = %s", (comp_id,))
                if cur.fetchone() is not None:
                    raise AccessError("You are not a participant in this Competition")
                
                raise InputError("Invalid competition")
            
            is_moderator, is_active_comp = result
            print(result)
            
            if not is_moderator:
                raise AccessError("You must be a moderator to end this competition")
            elif not is_active_comp:
                raise InputError("This competition has already ended")
            
            qry2 = """
                UPDATE Competitions
                SET is_active = %s, end_time = %s
                WHERE id = %s
                ;
            """
            qry2_params = [False, datetime.datetime.now().isoformat(), comp_id]
            
            cur.execute(qry2, qry2_params)
            
            conn.commit()

'''
Get a competition's leaderboard

Parameters
    - auth_user_id - the id of the user wanting to end the competition
    - comp_id - the competition id
    
Exceptions
    - InputError when
        - The provided start is greater than the total number of participants in the competition
        - The comp_id is invalid
    - AccessError if the user attempting to view the leaderboard is not a member
    
Returns
    - leaderboard - a list containing up to 10 participants and their rank
    - start - the index of the first participant
    - end - the index of the last participant; is -1 if there are less than 10.
'''
@sec.authorise
def leaderboard(auth_user_id, comp_id, start):
    with database.get_conn() as conn:
        with conn.cursor() as cur:
            qry1 = """
                SELECT player, competition
                FROM   CompetitionParticipants
                WHERE  player = %s
                AND    competition = %s
            """
            cur.execute(qry1, (auth_user_id, comp_id))
            if cur.fetchone() is None:
                cur.execute("SELECT id FROM Competitions WHERE id = %s", (comp_id,))
                if cur.fetchone() is not None:
                    raise AccessError("You are not a participant in this Competition")
                
                raise InputError("Invalid competition")
            
            
            qry2 = """
                SELECT   p.id, p.handle_str, cp.score, cp.is_moderator
                FROM     Players p
                JOIN     CompetitionParticipants cp ON (p.id = cp.player)
                WHERE    cp.competition = %s
                ORDER BY cp.score DESC
                LIMIT    10
                OFFSET   %s
                ;
            """
            qry2_params = (comp_id, start)
            
            cur.execute(qry2, qry2_params)
            
            ret = [{
                'u_id'         : u_id,
                'username'     : username,
                'score'        : score,
                'is_moderator' : is_moderator
            } for u_id, username, score, is_moderator in cur.fetchall()]

            if len(ret) == 0:
                raise InputError("Start is greater than number of participants")
            elif len(ret) < 10:
                end = -1
            else:
                end = start + 10
                
            return {
                'leaderboard' : ret,
                'start'       : start,
                'end'         : end
            }

