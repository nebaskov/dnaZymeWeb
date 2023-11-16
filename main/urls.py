from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('contacts', views.contacts, name='contacts'),
    path('knowledgebase', views.knowledgebase, name='knowledgebase'),
    path('generation', views.generation, name='generation'),
    path('new_main', views.new_main, name='new_main')
]
