# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models

class AccessToken(models.Model):
    user = models.ForeignKey(User)
    token = models.CharField(max_length=64, null=False)

class Folder(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=20, null=False, unique=True)

    def get_public_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }

class File(models.Model):
	folder = models.ForeignKey(Folder)
	name = models.CharField(max_length=255, null=False)

	def get_public_dict(self):
		return {
			'id': self.id,
			'name': self.name
		}