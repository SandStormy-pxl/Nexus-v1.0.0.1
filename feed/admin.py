from django.contrib import admin
from .models import Post, Curtida, Comentario, Seguidor, Mensagem


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'autor', 'criado_em', 'tem_imagem', 'tem_video')
    list_filter = ('criado_em',)
    readonly_fields = ('criado_em',)

    def tem_imagem(self, obj):
        return bool(obj.imagem_b64)
    tem_imagem.boolean = True

    def tem_video(self, obj):
        return bool(obj.video_b64)
    tem_video.boolean = True


@admin.register(Curtida)
class CurtidaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'post', 'criado_em')


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('autor', 'post', 'criado_em')


@admin.register(Seguidor)
class SeguidorAdmin(admin.ModelAdmin):
    list_display = ('seguidor', 'seguido', 'criado_em')


@admin.register(Mensagem)
class MensagemAdmin(admin.ModelAdmin):
    list_display = ('remetente', 'destinatario', 'lida', 'criado_em')
