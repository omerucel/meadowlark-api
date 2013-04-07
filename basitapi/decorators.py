#-*- coding: utf-8 -*-

from basitapi.exception import ApiException

from django.contrib.auth.models import User
from django.contrib.sessions.backends.db import SessionStore

def check_session(fn):
    def wrapped(self, request):
        session_key = request.REQUEST.get('session_key', '')
        session_store = SessionStore(session_key=session_key)
        if session_store == None or session_store.has_key('_auth_user_id') == False:
            raise ApiException("Unauthorized", status=401)

        try:
            user = User.objects.get(id=session_store['_auth_user_id'])
        except User.DoesNotExist, e:
            raise ApiException("Unauthorized", status=401)

        request.session_store = session_store
        request.user = user

        return fn(self, request)

    return wrapped
