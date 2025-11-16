from django.test import TestCase
from django.urls import reverse
from guarita.models import Chave

class TestChavesView(TestCase):
    
    def test_contexto_opcoes_filtro(self):
        # Acesse a view
        response = self.client.get(reverse('chaves')) #Quem eu quero testar
     
        # Verifica se 'opcoes_filtro' está no contexto
        self.assertIn('opcoes_filtro', response.context) # o que eu quero testar
        # Verifica o conteúdo esperado
        esperado = [
            ('disponivel', 'Disponível'),
            ('indisponivel', 'Indisponível'),
        ]

        self.assertEqual(response.context['opcoes_filtro'], esperado) #como eu quero que funcione

        