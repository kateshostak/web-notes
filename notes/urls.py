from django.conf.urls import url
from . import views

app_name = 'notes'

urlpatterns = [
    url(r'^(?P<username>[a-zA-Z0-9]+)/$', views.show_user_notes, name='show_user_notes'),
    url(r'^(?P<username>[a-zA-Z0-9]+)/add/$', views.add_note, name='add_note'),
    url(r'^(?P<username>[a-zA-Z0-9]+)/addlist/$', views.add_note_list, name='add_note_list'),
    url(r'^(?P<username>[a-zA-Z0-9]+)/delete/$', views.delete_notes, name='delete_notes'),
    url(r'^(?P<username>[a-zA-Z0-9]+)/search/$', views.search, name='search'),
    url(r'^(?P<username>[a-zA-Z0-9]+)/deletelist/$', views.delete_note_list, name='delete_note_list'),
]
