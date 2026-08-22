from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'criado_em', 'tem_imagem', 'tem_video')
    list_filter = ('criado_em',)
    readonly_fields = ('criado_em',)

    def tem_imagem(self, obj):
        return bool(obj.imagem_b64)
    tem_imagem.boolean = True
    tem_imagem.short_description = 'Imagem?'

    def tem_video(self, obj):
        return bool(obj.video_b64)
    tem_video.boolean = True
    tem_video.short_description = 'Vídeo?'
