# sua_app/middleware.py
from django.shortcuts import redirect
from django.urls import reverse


class ForcePasswordChangeMiddleware:
    """
    Middleware que força a alteração de senha no primeiro acesso
    ou quando definido pelo sistema.

    Este middleware intercepta todas as requisições autenticadas e
    verifica o atributo ``must_change_password`` vinculado à entidade
    ``Pessoa`` associada ao usuário logado.

    Regras de funcionamento:
        - Aplica-se apenas a usuários autenticados.
        - Superusuários são ignorados.
        - Caso ``must_change_password`` seja verdadeiro, o usuário é
          redirecionado para a página de alteração de senha.
        - As rotas de alteração de senha e logout não sofrem redirecionamento,
          evitando loop infinito.

    Fluxo:
        1. Obtém o usuário da requisição.
        2. Verifica autenticação.
        3. Ignora superusuários.
        4. Recupera a instância ``Pessoa`` relacionada.
        5. Se a flag estiver ativa, força redirecionamento.

    Attributes:
        get_response (Callable): Próximo middleware ou view da cadeia.
    """

    def __init__(self, get_response):
        """
        Inicializa o middleware.

        Args:
            get_response (Callable): Função que representa o próximo
            processamento da requisição.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Processa cada requisição HTTP recebida.

        Verifica se o usuário deve obrigatoriamente alterar a senha
        antes de continuar navegando no sistema.

        Args:
            request (HttpRequest): Objeto da requisição.

        Returns:
            HttpResponse: Resposta original ou redirecionamento
            para a tela de mudança de senha.
        """
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
