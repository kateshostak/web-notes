from django.conf.urls import url
from . import views

app_name = 'notes'

urlpatterns = [
    url(r'^(?P<username>[a-zA-Z0-9]+)/$', views.show_user_notes, name='show_user_notes'),
    url(r'^(?P<username>[a-zA-Z0-9]+)/add/$', views.add_note, name='add_note'),
    url(r'^(?P<username>[a-zA-Z0-9]+)/delete/$', views.delete_notes, name='delete_notes'),
    url(r'^(?P<username>[a-zA-Z0-9]+)/search/$', views.search, name='search'),
]
