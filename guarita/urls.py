from django.conf import settings
from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('atualizar-status/', views.atualizar_status, name='atualizar_status'),
    path('', views.status_chave, name='status_chaves'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path("relatorios/excel/", views.gerar_relatorio_excel, name="relatorio_excel"),
]

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()

