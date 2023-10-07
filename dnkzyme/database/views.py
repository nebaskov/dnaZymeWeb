from django.shortcuts import render
from .models import MainDataBase
from django.core import serializers


def database_home(request):
    db = serializers.serialize("python", MainDataBase.objects.all())
    return render(request, 'database/database_home.html', {'db': db})


def create(request):
    return render(request, 'database/create.html')
