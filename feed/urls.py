from django.urls import path
from . import views

urlpatterns = [
    path('', views.feed, name='feed'),
    path('postar/', views.criar_post, name='criar_post'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cadastro/', views.signup_view, name='signup'),
    path('busca/', views.busca, name='busca'),
    path('perfil/<str:username>/', views.perfil, name='perfil'),
    path('seguir/<str:username>/', views.seguir, name='seguir'),
    path('post/<int:post_id>/', views.post_detalhe, name='post_detalhe'),
    path('post/<int:post_id>/curtir/', views.curtir, name='curtir'),
    path('post/<int:post_id>/compartilhar/', views.compartilhar, name='compartilhar'),
    path('chat/', views.chat_lista, name='chat_lista'),
    path('chat/<str:username>/', views.chat_conversa, name='chat_conversa'),
]
