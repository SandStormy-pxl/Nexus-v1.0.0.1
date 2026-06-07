from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    texto = models.TextField(blank=True, null=True)
    imagem_b64 = models.TextField(blank=True, null=True)
    video_b64 = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    exclusivo_melhores_amigos = models.BooleanField(default=False)
    class Meta:
        ordering = ['-criado_em']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return f'Post #{self.id} — @{self.autor.username} — {self.criado_em.strftime("%d/%m/%Y %H:%M")}'
from django.db import models
from django.contrib.auth.models import User

class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    banido = models.BooleanField(default=False, verbose_name="Usuário Banido")

    def __str__(self):
        return f"Perfil de {self.user.username} - Banido: {self.banido}"

class IPRegistrado(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ips_registrados')
    endereco_ip = models.GenericIPAddressField(verbose_name="Endereço IP")
    data_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "IP Registrado"
        verbose_name_plural = "IPs Registrados"
        unique_together = ('user', 'endereco_ip') # Evita duplicar o mesmo IP para o mesmo usuário

    def __str__(self):
        return f"{self.endereco_ip} (@{self.user.username})"


from django.db import models

class ConfiguracaoSistema(models.Model):
    modo_manutencao = models.BooleanField(default=False, verbose_name="Ativar Modo Manutenção")
    mensagem_manutencao = models.TextField(
        default="O Nexus está em manutenção para melhorias. Voltamos logo!",
        verbose_name="Mensagem de Aviso"
    )

    exibir_alerta_geral = models.BooleanField(default=False, verbose_name="Exibir Alerta Geral no Topo")
    texto_alerta_geral = models.TextField(
        default="Aviso importante para todos os usuários!", 
        verbose_name="Texto do Alerta Geral"
    )

    class Meta:
        verbose_name = "Configuração do Sistema"
        verbose_name_plural = "Configurações do Sistema"

    def __str__(self):
        return f"Modo Manutenção: {'LIGADO' if self.modo_manutencao else 'DESLIGADO'}"


from django.db import models
from django.contrib.auth.models import User

# Adiciona isto no final do teu feed/models.py:
class Seguidor(models.Model):
    seguidor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seguindo')
    # Garanta que o nome desta variável abaixo seja 'seguido'
    seguido = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seguidores')
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('seguidor', 'seguido')

    def __str__(self):
        return f"{self.seguidor.username} segue {self.seguido.username}"

from django.db import models
from django.contrib.auth.models import User

# --- CURTIDAS ---
class Curtida(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='curtidas')
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'post') # Impede curtir o mesmo post duas vezes

# --- COMENTÁRIOS ---
class Comentario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comentarios')
    texto = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

# --- CHAT / MENSAGENS DIRETAS ---
class MensagemChat(models.Model):
    remetente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensagens_enviadas')
    destinatario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensagens_recebidas')
    texto = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['criado_em'] # Chat listado em ordem cronológica normal
