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
