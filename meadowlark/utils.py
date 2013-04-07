
from basitapi.response import ApiResponse

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