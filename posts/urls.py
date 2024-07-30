from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('create/', views.post_create, name='post_create'),
    path('detail/<int:pk>/', views.post_detail, name='post_detail'),
    path('feed/', views.feed, name='feed'),
    path('like/<int:pk>/', views.toggle_like, name='post_like'),
    path('friends_feed/', views.friends_feed, name='friends_feed'),
]
