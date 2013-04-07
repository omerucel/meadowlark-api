# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django import forms

from meadowlark import models

class UsersPostForm(forms.Form):
    username = forms.CharField(required=True, max_length=16, min_length=3)
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=8)

    def is_valid(self):
    	valid = super(UsersPostForm, self).is_valid()

    	if valid:
    		if User.objects.filter(username__exact=self.cleaned_data['username']).count() > 0:
    			self._errors['username'] = [u'username already in use']

    		if User.objects.filter(email__exact=self.cleaned_data['email']).count() > 0:
    			self._errors['email'] = [u'email already in use']

    		if bool(self._errors):
    			return False

    	return valid

class AccessTokensPostForm(forms.Form):
	email = forms.EmailField(required=False)
	username = forms.CharField(required=False, max_length=16, min_length=3)
	password = forms.CharField(required=True, min_length=8)

	def is_valid(self):
		valid = super(AccessTokensPostForm, self).is_valid()

		if self.data.has_key('email') == False and self.data.has_key('username') == False:
			self._errors['email'] = [u'email or username required']
			self._errors['username'] = [u'email or username required']
			return False

		return valid

class FoldersPostForm(forms.Form):
	name = forms.CharField(required=True, max_length=20)

	def is_valid(self, current_user):
		valid = super(FoldersPostForm, self).is_valid()

		if valid:
			if models.Folder.objects.filter(user__id=current_user.id, name__exact=self.cleaned_data['name']).count() > 0:
				self._errors['name'] = [u'name already in use']
				return False

		return valid

class FolderFilesPostForm(forms.Form):
	file = forms.FileField(required=True)