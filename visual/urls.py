from django.conf.urls import url
from django.contrib import admin
from visual import views as visual_views

urlpatterns = [
    url(r'^image$', visual_views.image, name='image'),
    url(r'^docker_pull_image$', visual_views.docker_pull_image, name='docker_pull'),
    url(r'^image_table$', visual_views.image_table, name='image_table'),
    url(r'^image_add$', visual_views.image_add, name='image_add'),
    url(r'^image_del$', visual_views.image_del, name='image_del'),
    url(r'^image_commit$', visual_views.image_commit, name='image_commit'),
    url(r'^image_dockerfile$', visual_views.image_dockerfile, name='image_dockerfile'),

    url(r'^container_table$', visual_views.container_table, name='container_table'),
    url(r'^container$', visual_views.container, name='container'),
    url(r'^container_add$', visual_views.container_add, name='container_add'),
    url(r'^docker_create_container$', visual_views.docker_create_container, name='docker_create_container'),
    url(r'^container_rm$', visual_views.container_rm, name='container_rm'),
    url(r'^container_start', visual_views.container_start, name='container_start'),
    url(r'^container_stop', visual_views.container_stop, name='container_stop'),
    url(r'^container_pause', visual_views.container_pause, name='container_pause'),
    url(r'^container_unpause', visual_views.container_unpause, name='container_unpause'),
]