from django import forms
from .fields import DataListWidget
from .models import Note, SimpleUser
from django.core import validators


def get_tags(author):
    note_tags = set([note.tag.lower() for note in author.note_set.all()])
    return [(tag, tag) for tag in note_tags]


def get_years(author):
    return [date.year for date in author.note_set.dates('date', 'year')]


def get_status(author):
    return author.note_set.model.STATUS_CHOICES


class NoteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.tags = set(kwargs.pop('tags'))
        super(NoteForm, self).__init__(*args, **kwargs)
        maxlen = Note._meta.get_field('tag').max_length
        self.fields['tag'].widget = DataListWidget(
            data_list=self.tags,
            name='tags'
        )
        self.fields['tag'].widget.attrs['maxlength'] = maxlen

    class Meta:
        model = Note
        fields = ['text', 'tag', 'status']

    def clean_tag(self):
        tag = self.cleaned_data['tag']
        return self.cleaned_data['tag']


class SearchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.years = kwargs.pop('years')
        self.tags = set(kwargs.pop('tags'))
        self.status = set(kwargs.pop('status'))
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['date'].widget = forms.SelectDateWidget(years=self.years)
        self.fields['tag'].widget = forms.Select(choices=self.tags)
        self.fields['status'].widget = forms.Select(choices=self.status)

    keyword = forms.CharField(required=False)
    tag = forms.ChoiceField(required=False)
    status = forms.ChoiceField(required=False)
    date = forms.DateField(required=False)
