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
                
                request_id = cur.fetchone()
            
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

def requests():
    pass

def approve(auth_user_id, request_id):
    pass

def reject(auth_user_id, request_id):
    pass

def override(auth_user_id, u_id, new_points):
    pass