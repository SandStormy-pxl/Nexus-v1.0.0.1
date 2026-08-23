import base64
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from .models import Post, Curtida, Comentario, Seguidor, Mensagem
from .forms import PostForm, LoginForm, SignupForm, ComentarioForm, MensagemForm


# ── AUTH ──────────────────────────────────────────────

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


# ── FEED ──────────────────────────────────────────────

@login_required(login_url='login')
def feed(request):
    posts = Post.objects.all()
    curtidas_usuario = set(
        Curtida.objects.filter(usuario=request.user).values_list('post_id', flat=True)
    )
    msgs_nao_lidas = Mensagem.objects.filter(destinatario=request.user, lida=False).count()
    return render(request, 'feed/feed.html', {
        'posts': posts,
        'curtidas_usuario': curtidas_usuario,
        'msgs_nao_lidas': msgs_nao_lidas,
    })


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


# ── CURTIR ────────────────────────────────────────────

@login_required(login_url='login')
def curtir(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    curtida, criada = Curtida.objects.get_or_create(usuario=request.user, post=post)
    if not criada:
        curtida.delete()
        curtido = False
    else:
        curtido = True
    total = post.curtidas.count()
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'curtido': curtido, 'total': total})
    return redirect(request.META.get('HTTP_REFERER', 'feed'))


# ── COMENTAR ──────────────────────────────────────────

@login_required(login_url='login')
def post_detalhe(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comentarios = post.comentarios.all()
    curtidas_usuario = set(
        Curtida.objects.filter(usuario=request.user).values_list('post_id', flat=True)
    )
    form = ComentarioForm()
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            Comentario.objects.create(
                autor=request.user,
                post=post,
                texto=form.cleaned_data['texto']
            )
            return redirect('post_detalhe', post_id=post.id)
    return render(request, 'feed/post_detalhe.html', {
        'post': post,
        'comentarios': comentarios,
        'form': form,
        'curtidas_usuario': curtidas_usuario,
    })


# ── SEGUIR ────────────────────────────────────────────

@login_required(login_url='login')
def seguir(request, username):
    usuario_alvo = get_object_or_404(User, username=username)
    if usuario_alvo == request.user:
        return redirect('perfil', username=username)
    seguindo, criado = Seguidor.objects.get_or_create(seguidor=request.user, seguido=usuario_alvo)
    if not criado:
        seguindo.delete()
    return redirect('perfil', username=username)


# ── PERFIL ────────────────────────────────────────────

@login_required(login_url='login')
def perfil(request, username):
    usuario = get_object_or_404(User, username=username)
    posts = Post.objects.filter(autor=usuario)
    curtidas_usuario = set(
        Curtida.objects.filter(usuario=request.user).values_list('post_id', flat=True)
    )
    ja_segue = Seguidor.objects.filter(seguidor=request.user, seguido=usuario).exists()
    total_seguidores = usuario.seguidores.count()
    total_seguindo = usuario.seguindo.count()
    return render(request, 'feed/perfil.html', {
        'usuario': usuario,
        'posts': posts,
        'ja_segue': ja_segue,
        'total_seguidores': total_seguidores,
        'total_seguindo': total_seguindo,
        'curtidas_usuario': curtidas_usuario,
    })


# ── BUSCA ─────────────────────────────────────────────

@login_required(login_url='login')
def busca(request):
    query = request.GET.get('q', '').strip()
    resultados = []
    if query:
        resultados = User.objects.filter(username__icontains=query).exclude(id=request.user.id)
    return render(request, 'feed/busca.html', {'query': query, 'resultados': resultados})


# ── CHAT ──────────────────────────────────────────────

@login_required(login_url='login')
def chat_lista(request):
    msgs = Mensagem.objects.filter(
        Q(remetente=request.user) | Q(destinatario=request.user)
    ).order_by('-criado_em')

    conversas = {}
    for msg in msgs:
        outro = msg.destinatario if msg.remetente == request.user else msg.remetente
        if outro.id not in conversas:
            conversas[outro.id] = {'usuario': outro, 'ultima': msg}

    for uid, dados in conversas.items():
        count = Mensagem.objects.filter(
            remetente=dados['usuario'], destinatario=request.user, lida=False
        ).count()
        dados['nao_lidas'] = count

    msgs_nao_lidas = Mensagem.objects.filter(destinatario=request.user, lida=False).count()

    return render(request, 'feed/chat_lista.html', {
        'conversas': conversas.values(),
        'msgs_nao_lidas': msgs_nao_lidas,
    })



@login_required(login_url='login')
def chat_conversa(request, username):
    outro = get_object_or_404(User, username=username)

    # Marca como lidas
    Mensagem.objects.filter(remetente=outro, destinatario=request.user, lida=False).update(lida=True)

    mensagens = Mensagem.objects.filter(
        Q(remetente=request.user, destinatario=outro) |
        Q(remetente=outro, destinatario=request.user)
    ).order_by('criado_em')

    form = MensagemForm()
    if request.method == 'POST':
        form = MensagemForm(request.POST)
        if form.is_valid():
            texto = form.cleaned_data.get('texto')
            if texto:
                Mensagem.objects.create(
                    remetente=request.user,
                    destinatario=outro,
                    texto=texto,
                )
            return redirect('chat_conversa', username=username)

    msgs_nao_lidas = Mensagem.objects.filter(destinatario=request.user, lida=False).count()

    return render(request, 'feed/chat_conversa.html', {
        'outro': outro,
        'mensagens': mensagens,
        'form': form,
        'msgs_nao_lidas': msgs_nao_lidas,
    })


@login_required(login_url='login')
def compartilhar(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    usuarios = User.objects.exclude(id=request.user.id)
    if request.method == 'POST':
        destinatario_id = request.POST.get('destinatario_id')
        destinatario = get_object_or_404(User, id=destinatario_id)
        Mensagem.objects.create(
            remetente=request.user,
            destinatario=destinatario,
            post_compartilhado=post,
        )
        return redirect('chat_conversa', username=destinatario.username)
    return render(request, 'feed/compartilhar.html', {'post': post, 'usuarios': usuarios})
def doar(request):
    return render(request, 'feed/doar.html')