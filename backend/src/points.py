## Inlead - Points Management Functions
##
## Josh Ramos (josh-ramos-22)
## January 2023
##

from src import sec
from src.db import database
from src.error import InputError, AccessError
import datetime
import psycopg2

@sec.authorise
def log(auth_user_id, comp_id, points):
    with database.get_conn() as conn:
        with conn.cursor() as cur:
            qry = """
                SELECT c.end_time, cp.is_moderator, c.max_points_per_log, c.is_points_moderated
                FROM   Competitions c
                JOIN   CompetitionParticipants cp on (c.id = cp.competition)
                WHERE  cp.player = %s
                AND    c.id = %s
                ;
            """
            
            qry_params = [auth_user_id, comp_id]
            
            cur.execute(qry, qry_params)
            
            res = cur.fetchone()
            
            if res is None:
                raise InputError("We could not verify your membership in this competition")
            
            endtime, is_moderator, max_points_per_log, is_points_moderated = res
            
            if endtime:
                raise InputError("This competition has already ended")
            elif points > max_points_per_log:
                raise InputError(f"Cannot log more than {max_points_per_log} points at a time")
            
            request_id = -1
            print(is_points_moderated, is_moderator)
            if is_points_moderated and not is_moderator:
                qry2 = """
                    INSERT INTO PointsRequests(player, competition, points)
                    VALUES (%s, %s, %s)
                    RETURNING id
                    ;
                """
                qry2_params = [auth_user_id, comp_id, points]
                
                cur.execute(qry2, qry2_params)
                
                request_id = cur.fetchone()[0]
            
            else:
                qry2 = """
                    UPDATE CompetitionParticipants
                    SET    score = score + %s
                    WHERE  player = %s
                    AND    competition = %s
                    ;
                """
                qry2_params = [points, auth_user_id, comp_id]
                
                cur.execute(qry2, qry2_params)
                
            conn.commit()
            
            return {
                'request_id' : request_id
            }


"""
Return a list of pending points requests for a given competition

Parameters
- auth_user_id - id of user making the request
- comp_id - the competition id

Exceptions
- InputError - when the competition is invalid
- AccessError - when the user is not a moderator of the competition

Returns
- list of requests, which is of the shape (request_id, u_id, username, points)
"""
@sec.authorise
def request_list(auth_user_id, comp_id):
    with database.get_conn() as conn:
        with conn.cursor() as cur:
            # verify that the auth user is a mod
            qry = """
                SELECT is_moderator 
                FROM   CompetitionParticipants 
                WHERE  player = %s
                AND    competition = %s
                ;
            """
            cur.execute(qry, (auth_user_id, comp_id))
            
            res = cur.fetchone()
            if not res:
                raise InputError("We could not verify that you are a member of this competition")
            elif not res[0]:
                raise AccessError("You are not a moderator of this competition")
            
            qry2 = """
                SELECT pr.id, p.id, p.username, pr.points
                FROM   PointsRequests pr
                JOIN   Players p on (pr.player = p.id)
                WHERE  pr.competition = %s
                ;
            """
            cur.execute(qry2, (comp_id,))
            
            return {
                "requests" : [
                    {
                        "request_id" : request_id,
                        "u_id"     : user_id,
                        "username" : username,
                        "points"   : points
                    } for request_id, user_id, username, points in cur.fetchall()
                ]
            }


'''
Process a request id, checking if the user is authorised to approve or reject it
and returning the corresponding user_id, comp_id, and point value
'''
def process_request_id(auth_user_id, request_id):
    with database.get_conn() as conn:
        with conn.cursor() as cur:
            qry = """
                SELECT player, competition, points
                FROM   PointsRequests
                WHERE  id = %s
            """

            cur.execute(qry, (request_id,))
            res = cur.fetchone()
            if res is None:
                raise InputError("Invalid Points Request")
            u_id, comp_id, points = res
            
            # verify that the auth user is a mod
            qry2 = """
                SELECT is_moderator 
                FROM   CompetitionParticipants 
                WHERE  player = %s
                AND    competition = %s
            """
            cur.execute(qry2, (auth_user_id, comp_id))
            
            res = cur.fetchone()
            if not res or not res[0]:
                raise AccessError("You are not a moderator of this competition")
            
            return u_id, comp_id, points

'''
Delete a points request with the given request id
'''
def delete_request(request_id):
    with database.get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                DELETE FROM PointsRequests
                WHERE       id = %s
            """, (request_id,))
            
            conn.commit()


'''
Approve an existing points request, adding the points to the corresponding leaderboard
and deleting the request

Parameters
- auth_user_id
- request_id - The id of the request

'''
@sec.authorise
def approve(auth_user_id, request_id):
    res = process_request_id(auth_user_id, request_id)
    u_id, comp_id, points = res
    
    with database.get_conn() as conn:
        with conn.cursor() as cur:
            qry = """
                UPDATE CompetitionParticipants
                SET    score = score + %s
                WHERE  player = %s
                AND    competition = %s
                ;
            """
            qry_params = (points, u_id, comp_id)
            
            cur.execute(qry, qry_params)
            
            conn.commit()
    
    return {}
'''
Reject an existing points request, deleting the request

Parameters
- auth_user_id
- request_id - The id of the request

Returns None

'''
@sec.authorise
def reject(auth_user_id, request_id):
    process_request_id(auth_user_id, request_id)
    delete_request(request_id)
    
    return {}

'''
Override a player's score

Parameters
- auth_user_id - the id of the user making the request
- u_id - the id of the player that will have their points overridden
- comp_id - the id of the competition
- new_points - the new point value

Exceptions
- InputError when
    - The given competition does not exist
    - The requestee is not part of the competition
    - The player whose points will be overriden is not in the competition

Access Error When
    - The requestee is not a moderator in the competition.

Returns None

'''
@sec.authorise
def override(auth_user_id, u_id, comp_id, new_points):
    with database.get_conn() as conn:
        with conn.cursor() as cur:
            qry = """
                SELECT is_moderator, score
                FROM   CompetitionParticipants
                WHERE  player = %s
                AND    competition = %s
            """
            qry_params = (auth_user_id, comp_id)
            
            cur.execute(qry, qry_params)
            res = cur.fetchone()
            
            if res is None:
                raise InputError("We could not verify that you are a part of this competition")
            
            is_moderator, _ = res
            
            if not is_moderator:
                raise AccessError("Only moderators can override points")
            
            # Verify that player with u_id is also part of the comp
            cur.execute(qry, (u_id, comp_id))
            if cur.fetchone() is None:
                raise InputError("The provided player is not part of this competition")
            
            qry2 = """
                UPDATE CompetitionParticipants
                SET    score = %s
                WHERE  player = %s
                AND    competition = %s
                ;
            """
            qry2_params = (new_points, u_id, comp_id)
            
            cur.execute(qry2, qry2_params)
            
            conn.commit()
            
    return {}