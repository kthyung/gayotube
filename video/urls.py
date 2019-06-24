from django.urls import path
from . import views

urlpatterns = [
    path('', views.video_blank, name='index'),
    path('index/<int:year>', views.video_index, name='index'),
    path('index/p<int:year>', views.video_pop_index, name='index'),
    path('genre/<int:type>', views.video_genre, name='genre'),
    path('genre/p<int:type>', views.video_pop_genre, name='genre'),
    path('search', views.video_search, name='search'),
    path('list', views.video_list, name='list'),
    path('new', views.video_new, name='new'),
    path('video/<int:video_id>/', views.video_detail, name='detail'),
]
