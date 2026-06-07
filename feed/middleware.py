from django.shortcuts import redirect
from django.urls import reverse

class VerificarDadosPerfilMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. Verifica se o usuário está autenticado (logado)
        if request.user.is_authenticated:
            
            # Substitua 'atualizar_perfil' pelo NOME da rota (url name) da sua página de coleta
            url_coleta = reverse('coleta')
            url_logout = reverse('logout') # Permite que ele deslogue se quiser

            # Evita um loop infinito de redirecionamento se ele já estiver na página de coleta ou deslogando
            if request.path != url_coleta and request.path != url_logout:
                
                # 2. A LÓGICA CORE: Verifica se qualquer um dos campos está vazio ou apenas com espaços
                u = request.user
                if not u.first_name or not u.last_name or not u.email:
                    # Se faltar algo, redireciona imediatamente para a página de coleta
                    return redirect(url_coleta)

        response = self.get_response(request)
        return response
from django.http import HttpResponseForbidden
from .models import IPRegistrado, PerfilUsuario

class BloqueioPorIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. Captura o IP de quem está tentando acessar a página
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_atual = x_forwarded_for.split(',')[0].strip()
        else:
            ip_atual = request.META.get('REMOTE_ADDR')

        # 2. Verifica se esse IP está associado a algum usuário com perfil de banido ativo
        ip_banido = IPRegistrado.objects.filter(
            endereco_ip=ip_atual, 
            user__perfil__banido=True
        ).exists()

        # 3. Se o IP constar na lista de banidos, o servidor recusa o acesso imediatamente (Erro 403)
        if ip_banido:
            return HttpResponseForbidden("<h1>Acesso Recusado</h1><p>Conexão rejeitada pelo servidor de segurança.</p>")

        response = self.get_response(request)
        return response


from django.http import HttpResponse
from django.template import loader
from .models import ConfiguracaoSistema, IPRegistrado

class BloqueioSustentacaoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. PEGAR O IP ATUAL (Para manter a sua segurança de IPs banidos ativa)
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        ip_atual = x_forwarded_for.split(',')[0].strip() if x_forwarded_for else request.META.get('REMOTE_ADDR')

        # [Segurança anterior] Verifica IPs Banidos
        if IPRegistrado.objects.filter(endereco_ip=ip_atual, user__perfil__banido=True).exists():
            return HttpResponse("<h1>Acesso Recusado</h1>", status=403)

        # 2. LÓGICA DO MODO MANUTENÇÃO
        # Se a pessoa estiver tentando acessar o painel administrativo (/admin), NÃO bloqueia.
        # Isso garante que você consiga entrar para desligar a manutenção depois!
        if not request.path.startswith('/admin'):
            config = ConfiguracaoSistema.objects.first()
            
            # Se a configuração existir e o modo manutenção estiver ativo
            if config and config.modo_manutencao:
                # E se quem está acessando NÃO for um administrador logado
                if not (request.user.is_authenticated and request.user.is_staff):
                    # Renderiza uma página HTML bonita de manutenção
                    template = loader.get_template('feed/manutencao.html')
                    context = {'mensagem': config.mensagem_manutencao}
                    return HttpResponse(template.render(context, request), status=503)

        response = self.get_response(request)
        return response
