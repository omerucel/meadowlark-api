#-*- coding: utf-8 -*-

class ApiException(Exception):
    """
    Beklenilen hatalar için kullanılır. Kullanıcıların düzgün bir şekilde bilgilendirilmesini sağlar.
    """
    def __init__(self, message="", status=400, application_code=None):
        self.message = message
        self.status = status
        self.application_code = application_code
