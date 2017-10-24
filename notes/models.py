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

    def get_by_status(self, status):
        return self.note_set.filter(status=status)


class Note(models.Model):
    NONE = "black"
    LOW = "green"
    NORMAL = "orange"
    URGENT = "red"

    STATUS_CHOICES = (
        (NONE, "None"),
        (LOW, "Low"),
        (NORMAL, "Normal"),
        (URGENT, "Urgent"),
    )

    author = models.ForeignKey(SimpleUser, on_delete=models.CASCADE, editable=False)
    text = models.CharField(max_length=200)
    date = models.DateTimeField('date created', editable=False)
    tag = models.CharField(max_length=20, default="other")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=NONE)

    def __str__(self):
        return self.text
