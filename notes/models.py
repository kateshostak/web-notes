from django.db import models

# Create your models here.


class SimpleUser(models.Model):
    user_login = models.CharField(max_length=10)

    def __str__(self):
        return self.user_login

    def get_all_notes(self):
        return self.note_set.all()


class Note(models.Model):
    author = models.ForeignKey(SimpleUser, on_delete=models.CASCADE)
    note_text = models.CharField(max_length=200)
    note_date = models.DateTimeField('date created')

    def __str__(self):
        return self.note_text
