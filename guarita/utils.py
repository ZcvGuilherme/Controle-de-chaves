from django.core.exceptions import PermissionDenied
from .models import Pessoa

def get_pessoa_from_user(user):
    try:
        return user.pessoa
    except Pessoa.DoesNotExist:
        raise PermissionDenied("Usuário não vinculado a uma pessoa.")