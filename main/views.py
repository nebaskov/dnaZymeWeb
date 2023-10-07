from django.shortcuts import render


def index(request):
    return render(request, 'main/base.html', {'title': "Home"})


def about(request):
    return render(request, 'main/index.html')
