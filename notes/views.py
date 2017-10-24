from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
from django.urls import reverse

from .models import SimpleUser, Note
from .forms import NoteForm, SearchForm


def user_notes(request, username):
    author = get_object_or_404(SimpleUser, login=username)
    note_years = [date.year for date in author.note_set.dates('date', 'year')]
    note_tags = set([note.tag.lower() for note in author.note_set.all()])

    note_tags_choices = list()
    for tag in note_tags:
        note_tags_choices.append((tag, tag))

    note_form = NoteForm(tags=note_tags_choices)
    search_form = SearchForm(years=note_years)
    context = {
        "username": username,
        "note_form": note_form,
        "search_form": search_form,
        "ordered_notes_list": author.get_all_notes().order_by('-date'),
    }
    return render(request, 'notes/notes.html', context)


def add_note(request, username):
    author = get_object_or_404(SimpleUser, login=username)
    note_years = [date.year for date in author.note_set.dates('date', 'year')]
    note_tags = set([note.tag.lower() for note in author.note_set.all()])

    note_tags_choices = list()
    for tag in note_tags:
        note_tags_choices.append((tag, tag))

    note_form = NoteForm(request.POST, tags=note_tags_choices)

    if note_form.is_valid():
        new_note = Note(
            text=note_form.cleaned_data['text'],
            tag=note_form.cleaned_data['tag'],
            status=note_form.cleaned_data['status'],
            date=timezone.now(),
            author=author,

        )
        new_note.save()
        return HttpResponseRedirect(
            reverse(
                'notes:user_notes',
                args=(username,)
            )
        )


def delete_notes(request, username):
    notes_id = request.POST.getlist('note_id')
    author = get_object_or_404(SimpleUser, login=username)
    note_to_delete = author.get_all_notes().filter(pk__in=notes_id)
    for note in note_to_delete:
        note.delete()

    return HttpResponseRedirect(
        reverse(
            'notes:user_notes',
            args=(username,)
        )
    )


def search(request, username):
    author = get_object_or_404(SimpleUser, login=username)
    search_form = SearchForm(request.GET)
    if search_form.cleaned_data['keyword']:
        found_notes = author.get_by_keyword(search_form.cleaned_data['keyword'])
    elif search_form.cleaned_data['tag']:
        found_notes = author.get_by_tag(search_form.cleaned_data['tag'])
    elif search_form.cleaned_data['status']:
        found_notes = author.get_by_status(search_form.cleaned_data['status'])
    else:
        found_notes = author.get_all_notes()

    context = {
        "username": username,
        "ordered_notes_list": found_notes.order_by('-date'),
    }
    return render(request, 'notes/notes.html', context)
