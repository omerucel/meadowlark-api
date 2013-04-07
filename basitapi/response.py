#-*- coding: utf-8 -*-

from django.utils import simplejson

from basitapi.exception import ApiException

class ApiResponse:
    """
    API yanıtlarının taşınması için kullanılır. Yanıtın düzgün bir şekilde istenilen formata çevirir.
    """
    def __init__(self, content={}, status=200):
        if isinstance(content, dict) == False:
            raise ApiException("'content' must be of type dict.", 500, 0)

        self.content = content
        self.status = status

    def to_json(self):
        return simplejson.dumps(self.content)

    def to_object(self):
        class Object:
            def __init__(self, kwargs):
                for i in kwargs:
                    setattr(self, i, kwargs[i])

        obj = Object(self.content)
        return obj
