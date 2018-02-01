from django.conf.urls import url
from connect import views as connect_views

urlpatterns = [
    url(r'^host_in_docker$', connect_views.host_in_docker, name='host_in_docker'),
    url(r'^post_docker_hosts$', connect_views.post_docker_hosts, name='post_docker_hosts'),
    url(r'^get_docker_hosts$', connect_views.get_docker_hosts, name='get_docker_hosts'),
]

