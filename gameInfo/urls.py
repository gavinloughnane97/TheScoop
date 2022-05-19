from django.urls import path

from . import views

app_name = 'gameInfo'
urlpatterns = [
    path('', views.index, name='index'),
    path('matchups', views.query_matchups, name='query_matchups'),
    path('<str:matchup_id>', views.detail, name='detail'),
]