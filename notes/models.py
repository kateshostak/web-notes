from django.db import models


class SimpleUser(models.Model):
    login = models.CharField(max_length=10)

    def __str__(self):
        return self.login

    def get_all_notes(self):
        return self.note_set.all()

    def get_by_tag(self, tag):
        return self.get_all_notes().filter(tag=tag)

    def get_by_keyword(self, keyword):
        return self.note_set.filter(text__contains=keyword)


class Note(models.Model):
    author = models.ForeignKey(SimpleUser, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    date = models.DateTimeField('date created')
    tag = models.CharField(max_length=20, default="other")

    def __str__(self):
        return self.text
