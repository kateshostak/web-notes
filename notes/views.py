from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
from django.urls import reverse

from .models import SimpleUser, Note
from .forms import NoteForm, SearchForm


def show_user_notes(request, username):
    author = get_object_or_404(SimpleUser, login=username)
    note_tags_choices = author.get_tags()
    note_years = author.get_years()
    status_choices = author.get_status()

    search_form = SearchForm(years=note_years, tags=note_tags_choices, status=status_choices)

    note_form = NoteForm(tags=note_tags_choices)

    context = {
        "username": username,
        "note_form": note_form,
        "search_form": search_form,
        "ordered_notes_list": author.get_all_notes().order_by('-date'),
    }
    return render(request, 'notes/notes.html', context)


def add_note(request, username):
    author = get_object_or_404(SimpleUser, login=username)
    note_tags_choices = author.get_tags()
    note_form = NoteForm(request.POST, tags=note_tags_choices)

    if note_form.is_valid():
        new_note = Note(
            text=note_form.cleaned_data['text'],
            tag=note_form.cleaned_data['tag'].lower(),
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
    id_list = request.POST.getlist('note_id')
    author = get_object_or_404(SimpleUser, login=username)
    note_to_delete = author.get_notes_by_ids(id_list)
    for note in note_to_delete:
        note.delete()

    return HttpResponseRedirect(
        reverse(
            'notes:show_user_notes',
            args=(username,)
        )
    )


def search(request, username):
    author = get_object_or_404(SimpleUser, login=username)
    note_years = author.get_years()
    note_tags_choices = author.get_tags()
    status_choices = author.get_status()

    search_form = SearchForm(
        request.GET,
        years=note_years,
        tags=note_tags_choices,
        status=status_choices
    )

    keyword = search_form['keyword'].value()
    tag = search_form['tag'].value()
    status = search_form['status'].value()

    notes = author.get_all_notes()
    found_notes = author.get_notes_by_params(keyword=keyword, tag=tag, status=status)

    context = {
        "username": username,
        "ordered_notes_list": found_notes.order_by('-date'),
    }
    return render(request, 'notes/notes.html', context)
