# sua_app/middleware.py
from django.shortcuts import redirect
from django.urls import reverse

class ForcePasswordChangeMiddleware:
    """
    <h2>Middleware para mudança de senha</h2>

    <p> Faz uma verificação se o atributo <b>must_change_password</b> do usuário é verdadeira, caso seja, o usuário é redirecionado para uma tela de redefinição de senha.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        if user.is_authenticated:
            # ignora superusuários
            if user.is_superuser:
                return self.get_response(request)

            pessoa = getattr(user, 'pessoa', None)

            if pessoa and pessoa.must_change_password:
                change_url = reverse('change_password')
                logout_url = reverse('logout')

                if request.path not in [change_url, logout_url]:
                    return redirect('change_password')

        return self.get_response(request)
