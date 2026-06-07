import requests
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

# Substitua pelo Token que você gerou no site do Pushbullet
PUSHBULLET_TOKEN = "o.HRzHFlSi49UMDNQIomOlhM6ZncQz9X5B"

@receiver(user_logged_in)
def enviar_notificacao_push(sender, request, user, **kwargs):
    url = "https://api.pushbullet.com/v2/pushes"
    
    # Configura os dados do Push
    dados = {
        "type": "note",
        "title": "🔐 Login Detectado no Nexus",
        "body": f"O usuário @{user.username} acabou de entrar na plataforma."
    }
    
    # Configura a autenticação da API
    headers = {
        "Access-Token": PUSHBULLET_TOKEN,
        "Content-Type": "application/json"
    }
    
    # Envia para o seu celular sem travar o site
    try:
        requests.post(url, json=dados, headers=headers, timeout=5)
    except Exception:
        pass
