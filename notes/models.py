from django.db import models
from django.db.models import Q


class SimpleUser(models.Model):
    login = models.CharField(max_length=100)

    def __str__(self):
        return self.login

    def get_all_notes(self):
        return self.note_set.all()

    def get_tags(self):
        note_tags = set([note.tag.lower() for note in self.note_set.all()])
        return [(tag, tag) for tag in note_tags]

    def get_years(self):
        return [date.year for date in self.note_set.dates('date', 'year')]

    def get_status(self):
        return self.note_set.model.STATUS_CHOICES

    def get_notes_by_ids(self, id_list):
        return self.note_set.filter(pk__in=id_list)

    def get_notes_by_params(self, keyword, tag, status):
        return self.note_set.all().filter(Q(text__contains=keyword) & Q(tag=tag) & Q(status__contains=status))

    def get_note_lists(self):
        return self.listofnotes_set.all()

    def get_note_list_by_name(self, name):
        return self.get_note_lists().filter(name=name)

class ListOfNotes(models.Model):
    author = models.ForeignKey(SimpleUser, on_delete=models.CASCADE, editable=False)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_all_notes(self):
        return self.note_set.all()


class Note(models.Model):
    NONE = ""
    LOW = "low"
    NORMAL = "normal"
    URGENT = "urgent"

    STATUS_CHOICES = (
        (NONE, ""),
        (LOW, "Low"),
        (NORMAL, "Normal"),
        (URGENT, "Urgent"),
    )

    author = models.ForeignKey(SimpleUser, on_delete=models.CASCADE, editable=False)
    note_list = models.ForeignKey(ListOfNotes, on_delete=models.CASCADE, editable=False, default=None)
    text = models.CharField(max_length=200)
    date = models.DateTimeField('date created', editable=False)
    tag = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=True)

    def __str__(self):
        return self.text
