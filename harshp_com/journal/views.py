from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render

from .models import JournalEntry, JournalSection, JournalTag


def auth(request):
    """Authenticate access to Journal"""
    # check if password is supplied via form
    if request.method == 'POST':
        password = request.POST.get('password', None)
        if password is None:
            return render(request, 'journal/auth.html')
        # authenticate the user is ME
        user = authenticate(username='harsh', password=password)
        # login the user
        if user is not None:
            login(request, user)
            return redirect('journal:entries:list')
    # for all other cases, show the journal auth page
    return render(request, 'journal/auth.html')


def tags(request):
    """Display all tags in journal"""
    if not request.user.is_authenticated():
        return redirect('journal:auth')
    tags = []
    for tag in JournalTag.objects.order_by('name').all():
        tags.append((tag, tag.entries.count()))

    return render(request, 'journal/tags.html', {'tags': tags})


def tag(request, slug):
    """Display posts associated with a tag"""
    if not request.user.is_authenticated():
        return redirect('journal:auth')
    tag = get_object_or_404(JournalTag, slug=slug)
    entries = tag.entries.order_by('date_published').all()
    return render(
        request, 'journal/tag.html',
        {'tag': tag, 'entries': entries})


def entries(request):
    """Display index of all entries"""
    if not request.user.is_authenticated():
        return redirect('journal:auth')
    entries = [
        (entry, True)
        for entry in
        JournalEntry.objects.order_by('-date_published')]

    sections = JournalSection.objects.order_by('name')
    return render(
        request, 'journal/entries.html', {
            'entries': entries,
            'private_sessions': len(sections) > 0, 'sections': sections})


def entry(request, entry_id):
    """Display journal entry"""
    if not request.user.is_authenticated():
        return redirect('journal:auth')
    entry = get_object_or_404(JournalEntry, id=entry_id)

    return render(request, 'journal/entry.html', {'entry': entry})


def sections(request):
    """Sections in the journal"""
    if not request.user.is_authenticated():
        return redirect('journal:auth')
    sections = []
    for section in JournalSection.objects.order_by('name').all():
        sections.append((section, section.entries.count()))
    return render(request, 'journal/sections.html', {'sections': sections})


def section(request, slug):
    """Section in the journal"""
    if not request.user.is_authenticated():
        return redirect('journal:auth')
    section = get_object_or_404(JournalSection, slug=slug)
    entries = section.entries\
        .filter(is_published=True).order_by('-date_published')
    return render(
        request, 'journal/section.html',
        {'entries': entries, 'section': section})


def logout_user(request):
    """Log out the user"""
    # log the user out IF they are logged in
    if request.user.is_authenticated():
        logout(request)
    return redirect('journal:auth')
