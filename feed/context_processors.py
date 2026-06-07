from .models import ConfiguracaoSistema

def alerta_sistema(request):
    config = ConfiguracaoSistema.objects.first()
    if config:
        return {
            'exibir_alerta': config.exibir_alerta_geral,
            'texto_alerta': config.texto_alerta_geral
        }
    return {
        'exibir_alerta': False,
        'texto_alerta': ""
    }
