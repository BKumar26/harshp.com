from django.shortcuts import render


def home(request):
    """hobby homepage"""
    return render(request, 'hobbies/homepage.html')
