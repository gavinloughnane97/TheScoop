from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'gameInfo'
urlpatterns = [
    path('', views.index, name='index'),
    path('matchups', views.query_matchups, name='query_matchups'),
    path('<str:matchup_id>', views.detail, name='detail'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
