from django.test import TestCase
from django.urls import reverse
from guarita.models import Chave

class TestChavesView(TestCase):
    def test_contexto_opcoes_filtro(self):
        # Acesse a view
        response = self.client.get(reverse('chaves'))
        print(response.context)
        # Verifica se 'opcoes_filtro' está no contexto
        self.assertIn('opcoes_filtro', response.context)

        # Verifica o conteúdo esperado
        esperado = [
            ('disponivel', 'Disponível'),
            ('indisponivel', 'Indisponível'),
        ]

        self.assertEqual(response.context['opcoes_filtro'], esperado)

    def test_exemplo_funciona(self):
        Chave.registrar_chave('Chave Teste')
        
        response = self.client.get(reverse('teste_views'))
        esperado = Chave.getAll()
        
        self.assertEqual(list(response.context['chaves']), list(esperado))
        