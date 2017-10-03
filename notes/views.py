from django.shortcuts import get_object_or_404, render

from .models import SimpleUser, Note


def index(request):
    return HttpResponse("Hello, world!")


def show_user_notes(request, username):
    user = get_object_or_404(SimpleUser, user_login=username)
    context = {
        'ordered_notes_list': user.get_all_notes().order_by('-note_date'),
    }
    return render(request, 'notes/notes.html', context)
