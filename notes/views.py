from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
from django.urls import reverse
from django.db.models import Q

from .models import SimpleUser, Note
from .forms import NoteForm, SearchForm, get_tags, get_years, get_status


def user_notes(request, username):
    author = get_object_or_404(SimpleUser, login=username)
    note_tags_choices = get_tags(author)
    note_years = get_years(author)
    status_choices = get_status(author)

    note_form = NoteForm(tags=note_tags_choices)
    search_form = SearchForm(years=note_years, tags=note_tags_choices, status=status_choices)

    context = {
        "username": username,
        "note_form": note_form,
        "search_form": search_form,
        "ordered_notes_list": author.get_all_notes().order_by('-date'),
    }
    return render(request, 'notes/notes.html', context)


def add_note(request, username):
    author = get_object_or_404(SimpleUser, login=username)
    note_tags_choices = get_tags(author)
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
    else:
        print("Hi!")
        for error in note_form.errors:
            print(str(error))
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
    note_years = get_years(author)
    note_tags_choices = get_tags(author)
    status_choices = get_status(author)

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
    found_notes = notes.filter(Q(text__contains=keyword) & Q(tag=tag) & Q(status__contains=status))

    context = {
        "username": username,
        "ordered_notes_list": found_notes.order_by('-date'),
    }
    return render(request, 'notes/notes.html', context)
