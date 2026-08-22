from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    texto = models.TextField(blank=True, null=True)
    imagem_b64 = models.TextField(blank=True, null=True)
    video_b64 = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criado_em']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return f'Post #{self.id} — @{self.autor.username}'


class Curtida(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='curtidas')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='curtidas')
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'post')

    def __str__(self):
        return f'@{self.usuario.username} curtiu Post #{self.post.id}'


class Comentario(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comentarios')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comentarios')
    texto = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['criado_em']

    def __str__(self):
        return f'@{self.autor.username} comentou no Post #{self.post.id}'


class Seguidor(models.Model):
    seguidor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seguindo')
    seguido = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seguidores')
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('seguidor', 'seguido')

    def __str__(self):
        return f'@{self.seguidor.username} segue @{self.seguido.username}'


class Mensagem(models.Model):
    remetente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensagens_enviadas')
    destinatario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensagens_recebidas')
    texto = models.TextField(blank=True, null=True)
    post_compartilhado = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True, blank=True, related_name='compartilhamentos')
    lida = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['criado_em']

    def __str__(self):
        return f'@{self.remetente.username} → @{self.destinatario.username}'
