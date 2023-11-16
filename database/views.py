from django.shortcuts import render
from .models import MainDnaDataBase
from django.core import serializers


def database_home(request):
    # db = serializers.serialize("python", MainDnaDataBase.objects.all())
    # return render(request, 'database/database_home.html', {'db': db})
    return render(request, 'database/database_home.html')

