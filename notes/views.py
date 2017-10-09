from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
from django.urls import reverse

from .models import SimpleUser, Note


def user_notes(request, username):
    author = get_object_or_404(SimpleUser, user_login=username)
    context = {
        "username": username,
        "ordered_notes_list": author.get_all_notes().order_by('-note_date'),
    }
    return render(request, 'notes/notes.html', context)


def add_note(request, username):
    note_text = request.POST['note_text']
    author = get_object_or_404(SimpleUser, user_login=username)
    if note_text:
        new_note = Note(
            note_text=note_text,
            note_date=timezone.now(),
            author=author
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
            "ordered_notes_list": author.get_all_notes().order_by('-note_date'),
            "error_message": "You didn't type any text.",
        }
        return render(request, 'notes/notes.html', context)
