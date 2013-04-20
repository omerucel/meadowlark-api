from django.conf.urls import patterns, include, url

from meadowlark import views

urlpatterns = patterns('',
    url(r'^api/v1/users$', views.UsersResource.as_view()),
    url(r'^api/v1/users/self$', views.UserSelfResource.as_view()),
    url(r'^api/v1/access-tokens$', views.AccessTokensResource.as_view()),
    url(r'^api/v1/access-tokens/self$', views.AccessTokenSelfResource.as_view()),
    url(r'^api/v1/endpoints/(?P<endpoint_id>\d+)/folders$', views.FoldersResource.as_view()),
    url(r'^api/v1/endpoints/(?P<endpoint_id>\d+)/folders/(?P<folder_id>\d+)$', views.FolderResource.as_view()),
    url(r'^api/v1/endpoints/(?P<endpoint_id>\d+)/folders/(?P<folder_id>\d+)/files$', views.FilesResource.as_view()),
    url(r'^api/v1/endpoints/(?P<endpoint_id>\d+)/folders/(?P<folder_id>\d+)/files/(?P<file_id>\d+)$', views.FileResource.as_view()),
)