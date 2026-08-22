import base64
from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm


def feed(request):
    posts = Post.objects.all()
    return render(request, 'feed/feed.html', {'posts': posts})


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
                tipo = imagem.content_type  # ex: image/jpeg
                encoded = base64.b64encode(dados).decode('utf-8')
                imagem_b64 = f'data:{tipo};base64,{encoded}'

            if video:
                dados = video.read()
                tipo = video.content_type  # ex: video/mp4
                encoded = base64.b64encode(dados).decode('utf-8')
                video_b64 = f'data:{tipo};base64,{encoded}'

            Post.objects.create(
                texto=texto,
                imagem_b64=imagem_b64,
                video_b64=video_b64,
            )
            return redirect('feed')
    else:
        form = PostForm()

    return render(request, 'feed/criar_post.html', {'form': form})
