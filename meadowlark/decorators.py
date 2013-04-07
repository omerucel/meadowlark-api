from django.core.exceptions import ObjectDoesNotExist
from basitapi.response import ApiResponse
from basitapi.exception import ApiException

from meadowlark import models
from meadowlark import utils


def access_token_required(fn):
    def wrapped(self, request, *args, **kwargs):
        access_token = request.REQUEST.get('access_token', '')
        try:
            access_token = models.AccessToken.objects.get(token=access_token)
        except ObjectDoesNotExist:
            return utils.get_unauthorized_error_response()

        request.user = access_token.user
        request.access_token = access_token

        return fn(self, request, *args, **kwargs)

    return wrapped

def load_model(model, id_name):
    def decorator(fn):
        def wrapped(self, request, *args, **kwargs):
            if kwargs.has_key(id_name):
                try:
                    request.folder = model.objects.get(id=kwargs[id_name])
                except ObjectDoesNotExist:
                    return ApiResponse({}, status=404)

            return fn(self, request, *args, **kwargs)

        return wrapped
    return decorator