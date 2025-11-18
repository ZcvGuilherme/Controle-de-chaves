from django.test import TestCase
from django.urls import reverse
from guarita.models import Chave, Pessoa, ChaveStatus
class TestChavesView(TestCase):
    
    def setUp(self):
         self.pessoa = Pessoa.objects.create(
             matricula=1,
             nome="João",
             cargo="Professor"
         )
         self.chave = Chave.objects.create(
             id=1,
             nome="Laboratório de Informática"
         )
         self.chave2 = Chave.registrar_chave("Lab 2")

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

    

#INFORMAÇÕES QUE SERÃO NECESSÁRIAS

#receber um objeto chaves que tenha:
#ChaveStatus
#Chaves



