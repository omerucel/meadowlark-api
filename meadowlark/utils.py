
import uuid
import hashlib
from basitapi.response import ApiResponse

from meadowlark import models

def get_unauthorized_error_response(data = None):
    if data == None:
        data = {
            'message': 'Unauthorized',
            'status': 401
        }

    return ApiResponse(data, status=401)

def get_validation_error_response(errors):
    return ApiResponse({
        'validation_errors': errors,
        'message': 'Validation Error',
        'status': 400
    }, status=400)

def get_user_private_data(user):
    return {
        'id' : user.id,
        'email': user.email,
        'username': user.username
    }

def create_access_token(user):
    access_token = models.AccessToken(user=user)
    access_token.token = hashlib.sha256('%s%s' %(uuid.uuid1(), user.email)).hexdigest()
    access_token.save()
    return access_token