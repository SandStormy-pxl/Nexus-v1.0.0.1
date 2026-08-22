from django.urls import path
from . import views

urlpatterns = [
    path('', views.feed, name='feed'),
    path('postar/', views.criar_post, name='criar_post'),
]
