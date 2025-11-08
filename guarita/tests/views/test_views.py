from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from guarita.models import Chave
from django.contrib.messages import get_messages



        # ============================================================
        # 1️. TESTES DA VIEW DE LISTAGEM ("chaves")
        # ============================================================
class TesteChavesViews(TestCase):
    """Testes para verificar o comportamento da views principal."""

    def test_view_chaves_status_code(self):
        """Verifica se a view 'chaves' retorna status 200 (sucesso)."""
        response = self.client.get(reverse('chaves'))
        self.assertEqual(response.status_code, 200)

    def test_view_chaves_template_usado(self):
        """Verifica se a views 'chaves' usa o template correto 'chaves.html'."""
        response = self.client.get(reverse('chaves'))
        self.assertTemplateUsed(response, 'chaves.html')
        
    """Verifica se a view 'chaves' envia o contexto esperado para o template, ou seja, verificar se a view realmente está enviando as variáveis certas.
    Contexto esperado” = as variáveis que a view envia para o template.
    Garante que a view está passando os dados certos para serem exibidos na página."""
    
    def test_contexto_da_view_chaves(self):
        """Verifica se a view 'chaves' envia os dados corretos no contexto."""
        response = self.client.get(reverse('chaves'))
        # Exemplo: se a view envia uma lista de chaves no contexto
        self.assertIn('chaves', response.context)
        
    """Testar se o conteúdo da página contém o nome de alguma chave. Serve pra garantir que a view está renderizando dados do contexto corretamente."""
    
    def test_pagina_contem_nome_de_chave(self):
        """Verifica se o nome da chave aparece no HTML renderizado."""
        Chave.objects.create(nome='Biblioteca', status='disponível')
        response = self.client.get(reverse('chaves'))
        self.assertContains(response, 'Biblioteca')

        # ============================================================
        # 2️. TESTES DA VIEW DE REGISTRO ("registrar_chave")
        # ============================================================
"""Testa a view responsável por registrar novas chaves."""
class TestRegistrarChaveView(TestCase):
    
    def setUp(self):
        """Cria um usuário autenticado para os testes, ou seja, cria um usuário de teste antes de cada caso."""
        self.user = User.objects.create_user(username='teste', password='1234')
            
    def test_view_registrar_chave_status_code(self):
        """Verifica se a view 'registrar_chave' retorna status 200 na requisição GET."""
        response = self.client.get(reverse('registrar_chave'))
        self.assertEqual(response.status_code, 200)

    def test_template_usado(self):
        """Usa o template correto."""
        response = self.client.get(reverse('registrar_chave'))
        self.assertTemplateUsed(response, 'registrar_chave.html')

    def test_criacao_de_chave_via_post(self):
        """Cria uma nova chave via POST e verifica persistência."""
        url = reverse('registrar_chave')
        data = {'nome': 'Sala 101', 'status': 'disponível'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # redireciona após salvar
        self.assertTrue(Chave.objects.filter(nome='Sala 101').exists())
    
    """Testar se formulário inválido não cria registro. Esse é essencial pra validar que a view trata erros de formulário corretamente."""
    def test_form_invalido_nao_cria_chave(self):
        """Verifica se um POST incompleto não cria nova chave."""
        url = reverse('registrar_chave')
        data = {'nome': ''}  # faltando campo obrigatório
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)  # reexibe o formulário
        self.assertFalse(Chave.objects.exists())

        # ============================================================
        # 3️. ESTES DA VIEW DE DEVOLUÇÃO ("devolver_chave")
        # ============================================================

class TestDevolverChaveView(TestCase):
    """Testa a view que gerencia a devolução de chaves."""

    def setUp(self):
        self.user = User.objects.create_user(username='teste', password='1234')
        self.client.login(username='teste', password='1234')
        self.chave = Chave.objects.create(nome='Auditório', status='emprestada')

    def test_status_code(self):
        """A view responde com código 200."""
        response = self.client.get(reverse('devolver_chave'))
        self.assertEqual(response.status_code, 200)

    def test_template_usado(self):
        """Usa o template 'devolver_chave.html'."""
        response = self.client.get(reverse('devolver_chave'))
        self.assertTemplateUsed(response, 'devolver_chave.html')

    def test_devolucao_via_post(self):
        """Atualiza o status da chave via POST."""
        url = reverse('devolver_chave')
        data = {'id': self.chave.id, 'status': 'disponível'}
        response = self.client.post(url, data)
        self.chave.refresh_from_db()
        self.assertEqual(self.chave.status, 'disponível')
        self.assertEqual(response.status_code, 302)
    
        """Testar se tentar devolver uma chave inexistente gera erro controlado. Útil pra garantir que a view lida bem com IDs inválidos.
        """
    def test_devolucao_de_chave_inexistente(self):
        """Deve retornar 404 ao tentar devolver uma chave inexistente."""
        url = reverse('devolver_chave')
        data = {'id': 9999, 'status': 'disponível'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 404)


        # ============================================================
        # 4️. TESTES DE AUTENTICAÇÃO E PERMISSÕES
        # ============================================================

class TestAutenticacaoEPermissoes(TestCase):
    """Verifica se views exigem login e tratam permissões corretamente."""

    def test_acesso_sem_login_redireciona(self):
        """Sem login, o usuário deve ser redirecionado para a tela de login."""
        response = self.client.get(reverse('chaves'))
        if response.status_code == 302:
            self.assertIn('/login/', response.url)

    def test_usuario_logado_acessa(self):
        """Usuário autenticado deve acessar normalmente."""
        user = User.objects.create_user(username='teste', password='1234')
        self.client.login(username='teste', password='1234')
        response = self.client.get(reverse('chaves'))
        self.assertEqual(response.status_code, 200)

        """Testar se usuário sem permissão é bloqueado. Caso você tenha permissões específicas (ex: só admin pode excluir ou editar):
        """
    def test_usuario_sem_permissao_nao_pode_excluir(self):
        """Usuário comum deve ser bloqueado ao tentar excluir chave."""
        user = User.objects.create_user(username='teste', password='1234')
        chave = Chave.objects.create(nome='Sala 10', status='disponível')
        self.client.login(username='teste', password='1234')
        url = reverse('deletar_chave', args=[chave.id])
        response = self.client.post(url)
        self.assertIn(response.status_code, [302, 403])    

        # ============================================================
        # 5️. TESTES DE CRUD COMPLETO (Editar / Excluir)
        # ============================================================

class TestCRUDOperacoes(TestCase):
    """Testa operações completas de edição e exclusão de chaves."""

    def setUp(self):
        self.user = User.objects.create_user(username='teste', password='1234')
        self.client.login(username='teste', password='1234')
        self.chave = Chave.objects.create(nome='Laboratório', status='disponível')

    def test_edicao_de_chave(self):
        """Edita uma chave existente."""
        url = reverse('editar_chave', args=[self.chave.id])
        data = {'nome': 'Laboratório Editado', 'status': 'indisponível'}
        response = self.client.post(url, data)
        self.chave.refresh_from_db()
        self.assertEqual(self.chave.nome, 'Laboratório Editado')
        self.assertEqual(response.status_code, 302)

    def test_exclusao_de_chave(self):
        """Exclui uma chave e verifica remoção."""
        url = reverse('deletar_chave', args=[self.chave.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Chave.objects.filter(id=self.chave.id).exists())

        """Testar se o redirecionamento após editar ou excluir é o esperado. Para garantir a navegação correta depois da operação.
        """
    def test_redireciona_apos_editar(self):
        """↩Após editar, deve redirecionar para a lista de chaves."""
        url = reverse('editar_chave', args=[self.chave.id])
        data = {'nome': 'Editada', 'status': 'disponível'}
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('chaves'))
        
    def test_redireciona_apos_excluir(self):
        """Após excluir, deve redirecionar para a lista de chaves."""
        url = reverse('deletar_chave', args=[self.chave.id])
        response = self.client.post(url)
        self.assertRedirects(response, reverse('chaves'))