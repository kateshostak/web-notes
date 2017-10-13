from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
from django.urls import reverse

from .models import SimpleUser, Note


def user_notes(request, username):
    author = get_object_or_404(SimpleUser, login=username)
    context = {
        "username": username,
        "ordered_notes_list": author.get_all_notes().order_by('-date'),
    }
    return render(request, 'notes/notes.html', context)


def add_note(request, username):
    note_text = request.POST['note_text']
    note_tag = request.POST['note_tag']
    author = get_object_or_404(SimpleUser, login=username)
    if note_text:
        new_note = Note(
            text=note_text,
            tag=note_tag,
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
    else:
        context = {
            "username": username,
            "ordered_notes_list": author.get_all_notes().order_by('-date'),
            "error_message": "You didn't type any text.",
        }
        return render(request, 'notes/notes.html', context)


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
    keyword = request.POST['keyword']
    note_tag = request.POST['note_tag']
    author = get_object_or_404(SimpleUser, login=username)
    if keyword:
        found_notes = author.get_by_keyword(keyword)
    elif note_tag:
        found_notes = author.get_by_tag(note_tag)
    else:
        found_notes = author.get_all_notes()

    context = {
        "username": username,
        "ordered_notes_list": found_notes.order_by('-date'),
    }
    return render(request, 'notes/notes.html', context)
