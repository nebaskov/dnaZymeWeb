from django.shortcuts import render
# from django.http import HttpResponse
from .models import Cofactor

# Create your views here.


def show_database(request):
    fields = [item.name for item in Cofactor._meta.get_fields()]
    data = [
        list(item.values()) for item in list(Cofactor.objects.all().values())
    ]
    return render(request, 'cofactor.html', {'fields': fields, 'data': data})
