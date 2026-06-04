from django.urls import path
from . import views

urlpatterns = [
    path('', views.feed, name='feed'),
    path('postar/', views.criar_post, name='criar_post'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cadastro/', views.signup_view, name='signup'),
]
