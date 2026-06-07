from django.urls import path
from . import views

urlpatterns = [
    path('', views.feed, name='feed'),
    path('postar/', views.criar_post, name='criar_post'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cadastro/', views.signup_view, name='signup'),
    path('users/', views.data_users, name='users'),
    path('coleta/', views.coleta_view, name='coleta'),
    path('p/<str:username>/', views.pagina_perfil, name='perfil'),
    path('p/<str:username>/seguir/', views.dar_seguir, name='dar_seguir'),
    path('post/<int:post_id>/curtir/', views.curtir_post, name='curtir_post'),
    path('post/<int:post_id>/', views.ver_post, name='ver_post'),
    path('chat/<str:username>/', views.sala_chat, name='chat'),
]
