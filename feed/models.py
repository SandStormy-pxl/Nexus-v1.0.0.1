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
