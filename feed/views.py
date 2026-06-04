import base64
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Post
from .forms import PostForm, LoginForm, SignupForm


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('feed')
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            User.objects.create_user(username=username, password=password)
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('feed')
    else:
        form = SignupForm()
    return render(request, 'feed/signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('feed')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('feed')
            else:
                messages.error(request, 'Usuário ou senha incorretos.')
    else:
        form = LoginForm()
    return render(request, 'feed/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def feed(request):
    posts = Post.objects.all()
    return render(request, 'feed/feed.html', {'posts': posts})


@login_required(login_url='login')
def criar_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            texto = form.cleaned_data.get('texto')
            imagem = form.cleaned_data.get('imagem')
            video = form.cleaned_data.get('video')

            imagem_b64 = None
            video_b64 = None

            if imagem:
                dados = imagem.read()
                tipo = imagem.content_type
                encoded = base64.b64encode(dados).decode('utf-8')
                imagem_b64 = f'data:{tipo};base64,{encoded}'

            if video:
                dados = video.read()
                tipo = video.content_type
                encoded = base64.b64encode(dados).decode('utf-8')
                video_b64 = f'data:{tipo};base64,{encoded}'

            Post.objects.create(
                autor=request.user,
                texto=texto,
                imagem_b64=imagem_b64,
                video_b64=video_b64,
            )
            return redirect('feed')
    else:
        form = PostForm()
    return render(request, 'feed/criar_post.html', {'form': form})
