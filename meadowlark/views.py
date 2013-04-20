# -*- coding: utf-8 -*-

import uuid
import hashlib

from basitapi.exception import ApiException
from basitapi.response import ApiResponse
from basitapi.views import ApiView

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from meadowlark import models
from meadowlark import forms
from meadowlark.decorators import access_token_required, load_model
from meadowlark import utils

# /users
class UsersResource(ApiView):
    def post(self, request):
        form = forms.UsersPostForm(request.REQUEST)
        if form.is_valid() == False:
            return utils.get_validation_error_response(form._errors)

        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        user = User.objects.create_user(username, email, password)
        user.is_staff = True
        user.save()

        access_token = utils.create_access_token(user)

        return ApiResponse({
            'user': utils.get_user_private_data(user),
            'token': access_token.token
        }, 201)

# /users/self
class UserSelfResource(ApiView):
    @access_token_required
    def get(self, request):
        return ApiResponse(utils.get_user_private_data(request.user))

# /access-tokens
class AccessTokensResource(ApiView):
    def post(self, request):
        form = forms.AccessTokensPostForm(request.REQUEST)
        if form.is_valid() == False:
            return utils.get_validation_error_response(form._errors)

        email = None
        username = None
        password = form.cleaned_data['password']
        if form.cleaned_data.has_key('email'):
            email = form.cleaned_data['email']
        if form.cleaned_data.has_key('username'):
            username = form.cleaned_data['username']

        if email == None or email.__len__() == 0:
            try:
                user = User.objects.get(username=username)
            except ObjectDoesNotExist:
                return utils.get_unauthorized_error_response()
        else:
            try:
                user = User.objects.get(email=email)
            except ObjectDoesNotExist:
                return utils.get_unauthorized_error_response()

        if user.check_password(password) == False:
            return utils.get_unauthorized_error_response()

        access_token = utils.create_access_token(user)

        return ApiResponse({
            'user': utils.get_user_private_data(user),
            'token': access_token.token
        }, 201)

    @access_token_required
    def delete(self, request):
        request.access_token.delete()
        return ApiResponse({}, 200);

# /access-tokens/self
class AccessTokenSelfResource(ApiView):
    @access_token_required
    def get(self, request):
        return ApiResponse({
            'user': utils.get_user_private_data(request.user),
            'token': request.access_token.token
        }, 200)

# /folders
class FoldersResource(ApiView):
    @access_token_required
    @load_model(model=models.Endpoint, id_name='endpoint_id', access_name='endpoint')
    def post(self, request, endpoint_id):
        form = forms.FoldersPostForm(request.REQUEST)
        if form.is_valid(request.user) == False:
            return utils.get_validation_error_response(form._errors)

        name = form.cleaned_data['name']

        folder = models.Folder(user=request.user, endpoint=request.endpoint, name=name)
        folder.save()

        return ApiResponse({
            'id': folder.id
        }, 201)

# /folders/:folder_id
class FolderResource(ApiView):
    @access_token_required
    @load_model(model=models.Folder, id_name = 'folder_id', access_name='folder')
    def get(self, request, folder_id):
        return ApiResponse(request.folder.get_public_dict())

# /folders/:folder_id/files
class FolderFilesResource(ApiView):
    @access_token_required
    @load_model(model=models.Folder, id_name='folder_id', access_name='folder')
    def get(self, request, folder_id):

        file_list = []
        for file in models.File.objects.filter(folder__id = request.folder.id).order_by('name').all():
            file_list.append(file.get_public_dict())

        return ApiResponse({
            'meta': {
                'total_record': file_list.__len__()
            },
            'files' : file_list,
        }, 200)

    @access_token_required
    @load_model(model=models.Folder, id_name='folder_id', access_name='folder')
    def post(self, request, folder_id):
        form = forms.FolderFilesPostForm(request.REQUEST, request.FILES)
        if form.is_valid() == False:
            return utils.get_validation_error_response(form._errors)

        file_item = models.File(folder=request.folder, file=form.cleaned_data['file'])
        file_item.save()

        return ApiResponse({
            'id': file_item.id
        },status=201)

# /files/:file_id
class FileResource(ApiView):
    @access_token_required
    @load_model(model=models.File, id_name='file_id', access_name='file')
    def get(self, request, file_id):
        return ApiResponse(request.file.get_public_dict(), status=200)