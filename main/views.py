from django.shortcuts import render


def index(request):
    return render(request, 'main/new_main.html', {'title': "Home"})


def contacts(request):
    return render(request, 'main/contacts.html')
