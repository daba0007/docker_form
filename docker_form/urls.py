
from django.conf.urls import url,include
from django.contrib import admin
from visual import views as visual_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^home$', visual_views.home, name='home'),
<<<<<<< HEAD
=======
    url(r'^$', visual_views.home, name='home'),

>>>>>>> 5b473a3b4defa7d2db70b799bf8bee179e63772f
    url(r'',include('visual.urls')),
    url(r'',include('connect.urls')),
    url(r'',include('user.urls')),
]
