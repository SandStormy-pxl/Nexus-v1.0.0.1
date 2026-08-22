from django.db import models


class Post(models.Model):
    texto = models.TextField(blank=True, null=True)
    imagem_b64 = models.TextField(blank=True, null=True)
    video_b64 = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criado_em']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return f'Post #{self.id} — {self.criado_em.strftime("%d/%m/%Y %H:%M")}'
