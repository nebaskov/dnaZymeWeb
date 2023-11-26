from django.urls import path
from . import views

urlpatterns = [
    path('knowledgebase', views.knowledgebase, name='knowledgebase'),
    path('introduction-to-dnazymes', views.article_1, name='introduction-to-dnazymes'),
    path('biochemical-assays', views.article_2, name='biochemical-assays'),
    path('recent-advancements', views.article_3, name='recent-advancements'),
    path('exploring-the-impact-of-sequence', views.article_4, name='exploring-the-impact-of-sequence'),
    path('strategies-for-predicting', views.article_5, name='strategies-for-predicting'),
    path('the-role-of-dnazymes', views.article_6, name='the-role-of-dnazymes'),
    path('challenges-and-future-prospects', views.article_7, name='challenges-and-future-prospects'),
    path('importance-of-dnazymes', views.article_8, name='importance-of-dnazymes'),

]
