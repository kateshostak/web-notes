from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<username>[a-zA-Z0-9]+)/$', views.show_user_notes, name='show_user_notes'),
]
