import requests
from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Post  # Certifique-se de que o nome do seu modelo de posts é 'Post'

PUSHBULLET_TOKEN = "o.HRzHFlSi49UMDNQIomOlhM6ZncQz9X5B"

# Função auxiliar para enviar o Push (evita repetir código)
def disparar_push(titulo, corpo):
    url = "https://api.pushbullet.com/v2/pushes"
    dados = {"type": "note", "title": titulo, "body": corpo}
    headers = {"Access-Token": PUSHBULLET_TOKEN, "Content-Type": "application/json"}
    try:
        requests.post(url, json=dados, headers=headers, timeout=5)
    except Exception:
        pass

# 1. SENSOR DE LOGIN (Você já tem esse)
@receiver(user_logged_in)
def enviar_notificacao_login(sender, request, user, **kwargs):
    disparar_push(
        titulo="🔐 Login Detectado",
        corpo=f"O usuário @{user.username} acabou de entrar no Nexus."
    )

# 2. SENSOR DE NOVA CONTA CRIADA
@receiver(post_save, sender=User)
def enviar_notificacao_cadastro(sender, instance, created, **kwargs):
    # O 'created' é True apenas quando um novo usuário é inserido no banco
    if created:
        disparar_push(
            titulo="✨ Novo Usuário Cadastrado!",
            corpo=f"Opa! @{instance.username} acabou de criar uma conta no Nexus."
        )

# 3. SENSOR DE NOVO POST PUBLICADO
@receiver(post_save, sender=Post)
def enviar_notificacao_novo_post(sender, instance, created, **kwargs):
    # O 'created' garante que você só seja avisado em novos posts (e não em edições)
    if created:
        # Pega o autor do post (ajuste 'user' ou 'autor' dependendo do seu modelo)
        autor = instance.user.username
        
        # Corta o texto do post para não estourar a notificação
        resumo_texto = instance.texto[:50] + "..." if len(instance.texto) > 50 else instance.texto

        disparar_push(
            titulo="📝 Novo Post no Feed",
            corpo=f"@{autor} postou: \"{resumo_texto}\""
        )
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import PerfilUsuario, IPRegistrado

def obter_ip_cliente(request):
    # Captura o IP real mesmo se o site estiver atrás do proxy da Vercel
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@receiver(user_logged_in)
def registrar_ip_no_login(sender, request, user, **kwargs):
    # 1. Garante que o PerfilUsuario existe (se não existir, cria um)
    PerfilUsuario.objects.get_or_create(user=user)
    
    # 2. Captura o IP atual da requisição
    ip_atual = obter_ip_cliente(request)
    
    if ip_atual:
        # 3. Salva o IP na "lista" (tabela vinculada) se ele já não estiver lá
        IPRegistrado.objects.get_or_create(user=user, endereco_ip=ip_atual)
