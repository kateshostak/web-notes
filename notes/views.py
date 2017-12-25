from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
from django.urls import reverse

from .models import SimpleUser, Note, ListOfNotes
from .forms import NoteForm, SearchForm, ListOfNotesForm

#revrite everything to one view and multiple functions! (the proper methid for manipulating miltiple forms is to pass some variable with the request)


def show_user_notes(request, username):
    author = get_object_or_404(SimpleUser, login=username)
    note_tags_choices = author.get_tags()
    status_choices = author.get_status()
    note_years = author.get_years()

    note_form = NoteForm(tags=note_tags_choices)
    note_list_form = ListOfNotesForm()
    search_form = SearchForm(
        years=note_years,
        tags=note_tags_choices,
        status=status_choices
    )

    notes_by_list = dict()

    for note_list in author.get_note_lists():
        notes_by_list[note_list.name] = note_list.get_all_notes().order_by('-date')

    context = {
        "username": username,
        "note_form": note_form,
        "note_list_form": note_list_form,
        "search_form": search_form,
        "notes_by_list": notes_by_list,
    }
    return render(request, 'notes/notes.html', context)


def add_note(request, username):
    author = get_object_or_404(SimpleUser, login=username)
    list_name = request.POST.get("note_list_name")
    print(list_name)
    note_list = get_object_or_404(ListOfNotes, name=list_name)

    note_tags_choices = author.get_tags()
    note_form = NoteForm(request.POST, tags=note_tags_choices)
    if note_form.is_valid():
        new_note = Note(
            text=note_form.cleaned_data['text'],
            tag=note_form.cleaned_data['tag'].lower(),
            status=note_form.cleaned_data['status'],
            date=timezone.now(),
            author=author,
            note_list=note_list,

        )
        new_note.save()
    else:
        print("Invalid form")

    return HttpResponseRedirect(
        reverse(
            'notes:show_user_notes',
            args=(username,)
        )
    )


def delete_notes(request, username):
    id_list = request.POST.getlist('note_id')
    if id_list:
        author = get_object_or_404(SimpleUser, login=username)
        note_to_delete = author.get_notes_by_ids(id_list)
        for note in note_to_delete:
            note.delete()

    else:
        print("No ids selected")
    return HttpResponseRedirect(
        reverse(
            'notes:show_user_notes',
            args=(username,)
        )
    )


def add_note_list(request, username):
    author = get_object_or_404(SimpleUser, login=username)
    note_list_form = ListOfNotesForm(request.POST)

    if note_list_form.is_valid():
        new_list = ListOfNotes(
            name=note_list_form.cleaned_data['name'],
            author=author,
        )
        new_list.save()
    else:
        print("Invalid form")

    return HttpResponseRedirect(
        reverse(
            'notes:show_user_notes',
            args=(username,)
        )
    )

def delete_note_list(request, username):
    author = get_object_or_404(SimpleUser, login=username)
    list_name = request.POST.get('list_name')
    if list_name:
        note_list = author.get_note_list_by_name(list_name)
        note_list.delete()
    else:
        pritn('No lists selected.')

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
    return render(request, 'notes/found.html', context)
