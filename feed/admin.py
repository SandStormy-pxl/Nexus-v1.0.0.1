from django.contrib import admin
from .models import Post
from django.contrib.auth.models import Permission

admin.site.register(Permission)


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


from django.contrib import admin
from .models import PerfilUsuario, IPRegistrado

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('user', 'banido')
    list_editable = ('banido',)

@admin.register(IPRegistrado)
class IPRegistradoAdmin(admin.ModelAdmin):
    list_display = ('endereco_ip', 'user', 'data_registro')
    search_fields = ('endereco_ip', 'user__username')

