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
        return f'Post #{self.id} — @{self.autor.username} — {self.criado_em.strftime("%d/%m/%Y %H:%M")}'
