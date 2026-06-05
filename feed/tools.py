from django.db.models import Model
from django.forms.models import model_to_dict
def consulta_geral():
  queryset = Users.objects.all()
  for instance in queryset:
    users = model_to_dict(queryset)
    id = users['id']
    username = users['username']
    result = f"""
    id: {id}
    username: {username}
    .
    """
    return result