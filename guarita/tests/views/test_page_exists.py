# from django.test import TestCase
# from django.urls import reverse

# class ViewsTestCase(TestCase):

#     def test_view_chaves_status_code(self):
#         """Verifica se a view 'chaves' retorna status 200."""
#         response = self.client.get(reverse('chaves'))  # nome da rota no urls.py
#         self.assertEqual(response.status_code, 200)

#     def test_view_chaves_template_usado(self):
#         """Verifica se a view 'chaves' usa o template correto."""
#         response = self.client.get(reverse('chaves'))
#         self.assertTemplateUsed(response, 'chaves.html')

#     def test_view_registrar_chave_status_code(self):
#         """Verifica se a view 'registrar_chave' retorna status 200."""
#         response = self.client.get(reverse('registrar_chave'))
#         self.assertEqual(response.status_code, 200)

#     def test_view_registrar_chave_template_usado(self):
#         """Verifica se usa o template correto."""
#         response = self.client.get(reverse('registrar_chave'))
#         self.assertTemplateUsed(response, 'registrar_chave.html')

#     def test_view_devolver_chave_status_code(self):
#         """Verifica se a view 'devolver_chave' retorna status 200."""
#         response = self.client.get(reverse('devolver_chave'))
#         self.assertEqual(response.status_code, 200)

#     def test_view_devolver_chave_template_usado(self):
#         """Verifica se a view usa o template correto."""
#         response = self.client.get(reverse('devolver_chave'))
#         self.assertTemplateUsed(response, 'devolver_chave.html')
