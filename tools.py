from django.db.models import Model
from django.forms.models import model_to_dict
# LINHA CORRIGIDA: Importando o modelo User padrão do Django
from django.contrib.auth.models import User 

def obter_dados(tabela, quantos):
    dados = None
    
    if quantos == 'all':
        queryset = tabela.objects.all()
        dados = [model_to_dict(objeto) for objeto in queryset]
        
    elif isinstance(quantos, int):
        queryset = tabela.objects.get(id=quantos)
        dados = model_to_dict(queryset)
        
    elif isinstance(quantos, str):
        queryset = tabela.objects.get(username=quantos)
        dados = model_to_dict(queryset)
        
    return dados

# Agora o Python sabe o que significa 'User'
usuarios = obter_dados(User, 'all')
identify = usuarios['id']
username = usuarios['username']
resposta = f'''id: {id}
username: {username}'''
print(resposta)
