# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django import forms

from meadowlark import models

class UsersPostForm(forms.Form):
    username = forms.CharField(required=True, max_length=16, min_length=3, error_messages = {
        'required': 'required',
        'max_length': 'max_length',
        'min_length': 'min_length'
    })
    email = forms.EmailField(required=True, error_messages = {
        'required': 'required',
        'invalid': 'invalid'
    })
    password = forms.CharField(required=True, min_length=8, error_messages = {
        'required': 'required',
        'min_length': 'min_length'
    })

    def is_valid(self):
        valid = super(UsersPostForm, self).is_valid()

        if valid:
            if User.objects.filter(username__exact=self.cleaned_data['username']).count() > 0:
                self._errors['username'] = ['already-in-use']

            if User.objects.filter(email__exact=self.cleaned_data['email']).count() > 0:
                self._errors['email'] = ['already-in-use']

            if bool(self._errors):
                return False

        return valid

class AccessTokensPostForm(forms.Form):
    email = forms.EmailField(required=False, error_messages = {
        'invalid': 'invalid'
    })
    username = forms.CharField(required=False, max_length=16, min_length=3, error_messages = {
        'max_length': 'max_length',
        'min_length': 'min_length'
    })
    password = forms.CharField(required=True, min_length=8, error_messages = {
        'required': 'required',
        'min_length': 'min_length'
    })

    def is_valid(self):
        valid = super(AccessTokensPostForm, self).is_valid()

        if self.data.has_key('email') == False and self.data.has_key('username') == False:
            self._errors['email'] = ['required']
            self._errors['username'] = ['required']
            return False

        return valid

class FoldersPostForm(forms.Form):
    name = forms.CharField(required=True, max_length=20, error_messages = {
        'required': 'required',
        'max_length': 'max_length'
    })

    def is_valid(self, current_user):
        valid = super(FoldersPostForm, self).is_valid()

        if valid:
            if models.Folder.objects.filter(user__id=current_user.id, name__exact=self.cleaned_data['name']).count() > 0:
                self._errors['name'] = [u'name already in use']
                return False

        return valid

class FolderFilesPostForm(forms.Form):
    file = forms.FileField(required=True, error_messages = {
        'required': 'required'
    })