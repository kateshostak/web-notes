from django.contrib import admin
from .models import Note, SimpleUser

# Register your models here.
admin.site.register(Note)
admin.site.register(SimpleUser)
