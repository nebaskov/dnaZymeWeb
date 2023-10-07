from django.urls import path
from . import views


urlpatterns = [
    path('', views.database_home, name='database_home'),
    path('create', views.create, name='create')
]
