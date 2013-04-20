# -*- coding: utf-8 -*-

import os
from django.contrib.auth.models import User
from django.db import models

class AccessToken(models.Model):
    user = models.ForeignKey(User)
    token = models.CharField(max_length=64, null=False)

class Endpoint(models.Model):
    name = models.CharField(max_length=20, null=False, unique=True)

class Folder(models.Model):
    user = models.ForeignKey(User)
    endpoint = models.ForeignKey(Endpoint)
    name = models.CharField(max_length=20, null=False, unique=True)

    def get_public_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }

class File(models.Model):
    folder = models.ForeignKey(Folder)
    name = models.CharField(max_length=255, null=False)
    file = models.FileField(upload_to='files')

    def get_public_dict(self):
        name,extension = os.path.splitext(self.file.name)

        return {
            'id': self.id,
            'name': self.file.name,
            'size': self.file.size,
            'extension': extension
        }