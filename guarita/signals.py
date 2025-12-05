from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Chave, ChaveStatus, Historico, Pessoa
from django.contrib.auth.models import User
@receiver(post_save, sender=Chave)
def criar_status_automatico(sender, instance, created, **kwargs):
    if created:
        ChaveStatus.objects.get_or_create(chave=instance)


@receiver(post_save, sender=Chave)
def gerar_itemBusca(sender, instance, created, **kwargs):
    if created:
        instance.itemBusca = f"Chave {instance.id} - {instance.nome}"
        instance.save(update_fields=["itemBusca"])


@receiver(post_save, sender=Pessoa)
def criar_usuario_para_pessoa(sender, instance, created, **kwargs):
    if created and instance.user is None:
        user = User.objects.create_user(
            username=str(instance.matricula),
            password=str(instance.matricula),  # ou outra regra
            first_name=instance.nome
        )
        instance.user = user
        instance.save()


@receiver(post_save, sender=Pessoa)
def atualizar_usuario(sender, instance, created, **kwargs):
    if not created and instance.user:
        instance.user.first_name = instance.nome
        instance.user.save()
