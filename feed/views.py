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

    
