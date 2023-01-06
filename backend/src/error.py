## Inlead - Exception Types
##
## Reused from 2021 assignment 'UNSW Streams'

from werkzeug.exceptions import HTTPException

class AccessError(HTTPException):
    code = 403
    message = 'No message specified'

class InputError(HTTPException):
    code = 400
    message = 'No message specified'
