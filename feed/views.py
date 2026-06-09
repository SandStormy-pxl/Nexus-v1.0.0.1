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
def data_users(request):
  users = User.objects.all()
  return render(request, 'feed/users.html', {'users': users})

from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages

def coleta_view(request):
    if request.method == 'POST':
        # Coleta os dados enviados pelo HTML
        username_ref = request.POST.get('username_referencia')
        primeiro_nome = request.POST.get('first_name')
        ultimo_nome = request.POST.get('last_name')
        novo_email = request.POST.get('email')

        try:
            # Tenta buscar o usuário que possui ESSE username exato
            usuario = User.objects.get(username=username_ref)

            # Aplica as novas informações recebidas.
            # Se o campo estava vazio, ele preenche. Se continha dados, ele substitui (sobrescreve).
            usuario.first_name = primeiro_nome
            usuario.last_name = ultimo_nome
            usuario.email = novo_email

            # Salva a instância modificada no banco de dados
            usuario.save()

            messages.success(request, f"Usuário '{username_ref}' atualizado com sucesso!")

        except User.DoesNotExist:
            # Caso o username digitado não exista no banco de dados
            messages.error(request, f"Erro: O username '{username_ref}' não foi encontrado.")
            
        except Exception as e:
            # Captura qualquer outro erro inesperado (ex: e-mail duplicado se houver restrição)
            messages.error(request, "Ocorreu um erro ao salvar as informações.")

    return render(request, 'feed/coleta.html')
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required
def listar_usuarios_view(request):
    # Puxa todos os usuários cadastrados
    users = User.objects.all()
    
    return render(request, 'feed/users.html', {'users': users})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Post, Seguidor  # Importa do próprio app feed

@login_required
def pagina_perfil(request, username):
    perfil_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(autor=perfil_user).order_by('-id')
    
    # ATENÇÃO AQUI: Mudamos de alvo=perfil_user para seguido=perfil_user
    ja_segue = Seguidor.objects.filter(seguidor=request.user, seguido=perfil_user).exists()
    
    total_seguidores = perfil_user.seguidores.count()
    total_seguindo = perfil_user.seguindo.count()

    context = {
        'perfil_user': perfil_user,
        'posts': posts,
        'ja_segue': ja_segue,
        'total_seguidores': total_seguidores,
        'total_seguindo': total_seguindo,
    }
    return render(request, 'feed/perfil.html', context)

@login_required
def dar_seguir(request, username):
    alvo_user = get_object_or_404(User, username=username)
    
    if request.user != alvo_user:
        # ATENÇÃO AQUI: Mudamos de alvo=alvo_user para seguido=alvo_user
        seguindo_registro = Seguidor.objects.filter(seguidor=request.user, seguido=alvo_user)
        
        if seguindo_registro.exists():
            seguindo_registro.delete()
        else:
            # ATENÇÃO AQUI: Mudamos de alvo=alvo_user para seguido=alvo_user
            Seguidor.objects.create(seguidor=request.user, seguido=alvo_user)
            
    return redirect('perfil', username=username)

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Post, Curtida, Comentario, MensagemChat

# Função para Curtir/Descurtir
@login_required
def curtir_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    curtido_registro = Curtida.objects.filter(usuario=request.user, post=post)
    
    if curtido_registro.exists():
        curtido_registro.delete()
    else:
        Curtida.objects.create(usuario=request.user, post=post)
        
    # Retorna para a página onde o usuário estava (Feed ou Perfil)
    return redirect(request.META.get('HTTP_REFERER', 'feed'))

# Página de Detalhes do Post + Comentários
@login_required
def ver_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comentarios = post.comentarios.all().order_by('criado_em') # Antigos em cima, novos embaixo
    
    if request.method == 'POST':
        texto_comentario = request.POST.get('texto', '').strip()
        if texto_comentario:
            Comentario.objects.create(usuario=request.user, post=post, texto=texto_comentario)
        return redirect('ver_post', post_id=post.id)

    ja_curtiu = post.curtidas.filter(usuario=request.user).exists()

    context = {
        'post': post,
        'comentarios': comentarios,
        'ja_curtiu': ja_curtiu,
        'total_curtidas': post.curtidas.count()
    }
    return render(request, 'feed/ver_post.html', context)

# Chat Direto com um Usuário específico
@login_required
def sala_chat(request, username):
    outro_usuario = get_object_or_404(User, username=username)
    
    # Filtra as mensagens trocadas apenas entre você e essa pessoa
    mensagens = MensagemChat.objects.filter(
        (Q(remetente=request.user) & Q(destinatario=outro_usuario)) |
        (Q(remetente=outro_usuario) & Q(destinatario=request.user))
    )

    if request.method == 'POST':
        texto_mensagem = request.POST.get('mensagem', '').strip()
        if texto_mensagem:
            MensagemChat.objects.create(remetente=request.user, destinatario=outro_usuario, texto=texto_mensagem)
        return redirect('chat', username=username)

    return render(request, 'feed/chat.html', {'outro_usuario': outro_usuario, 'mensagens': mensagens})



from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages

def cadastrar_usuario(request):
    if request.method == 'POST':
        # Aqui você pega os dados que vieram do seu formulário HTML
        username = request.POST.get('username')
        senha = request.POST.get('password')
        email = request.POST.get('email') # É preciso coletar o e-mail do usuário!

        # 1. Validações básicas (exemplo rápido)
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Este username já existe.')
            return render(request, 'cadastro.html')

        # 2. Cria o usuário no banco de dados
        novo_usuario = User.objects.create_user(
            username=username, 
            password=senha, 
            email=email
        )
        
        # 3. DISPARO AUTOMÁTICO DO GMAIL
        # O Django vai rodar isso aqui sem que o usuário precise fazer nada
        try:
            send_mail(
                subject='Bem-vindo à nossa Rede Social! 🎉',
                message=f'Olá @{username},\n\nSua conta foi criada com sucesso! Aproveite a plataforma.',
                from_email=None, # Usa o DEFAULT_FROM_EMAIL do settings
                recipient_list=[email], # Manda para o e-mail que o usuário cadastrou
                fail_silently=True, # Se o Gmail falhar, não trava a tela de sucesso do usuário
            )
        except Exception as e:
            # Log do erro no seu terminal caso falhe, mas sem quebrar o site
            print(f"Erro ao enviar e-mail de boas-vindas: {e}")

        messages.success(request, 'Conta criada com sucesso! Verifique seu e-mail.')
        return redirect('login') # Redireciona para a tela de login

    return render(request, 'cadastro.html')
