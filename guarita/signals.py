from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Chave, ChaveStatus, Pessoa
from django.contrib.auth.models import User

@receiver(post_save, sender=Chave)
def criar_status_automatico(sender, instance, created, **kwargs):
    """
    <h2>Criação automática do status da chave</h2>\n
    Este signal é acionado após o salvamento de uma instância de <b>Chave</b>.\n

    <p>
    Quando uma nova chave é criada (<b>created=True</b>), este método garante
    que exista um registro correspondente na tabela <b>ChaveStatus</b>,
    inicializando o controle de disponibilidade da chave no sistema.
    </p>\n
    """
    if created:
        ChaveStatus.objects.get_or_create(chave=instance)


@receiver(post_save, sender=Chave)
def gerar_itemBusca(sender, instance, created, **kwargs):
    """
    <h2>Geração automática do campo itemBusca</h2>\n
    Este signal é acionado após o salvamento de uma instância de <b>Chave</b>.\n

    <p>
    Quando a chave é criada, o campo <b>itemBusca</b> é preenchido automaticamente
    com uma string padronizada contendo o identificador e o nome da chave.
    </p>\n

    <b>Formato gerado:</b> "Chave &lt;id&gt; - &lt;nome&gt;"\n
    """
    if created:
        instance.itemBusca = f"Chave {instance.id} - {instance.nome}"
        instance.save(update_fields=["itemBusca"])


@receiver(post_save, sender=Pessoa)
def criar_usuario_para_pessoa(sender, instance, created, **kwargs):
    """
    <h2>Criação automática de usuário Django</h2>\n
    Este signal é acionado após o salvamento de uma instância de <b>Pessoa</b>.\n

    <p>
    Caso a pessoa tenha sido criada (<b>created=True</b>) e ainda não possua
    um usuário associado, este método cria automaticamente um registro
    em <b>auth.User</b>.
    </p>\n

    <b>Regras aplicadas:</b>\n
    - O <b>username</b> é definido como a matrícula da pessoa.\n
    - A <b>senha inicial</b> é igual à matrícula (regra esta que deve ser alterada no deploy).\n
    - O <b>first_name</b> recebe o nome da pessoa.\n
    """
    if created and instance.user is None:
        user = User.objects.create_user(
            username=str(instance.matricula),
            password=str(instance.matricula),  # Mudar regra para senha aqui
            first_name=instance.nome
        )
        instance.user = user
        instance.save()


@receiver(post_save, sender=Pessoa)
def atualizar_usuario(sender, instance, created, **kwargs):
    """
    <h2>Sincronização de dados do usuário</h2>\n
    Este signal é acionado após o salvamento de uma instância de <b>Pessoa</b>.\n

    <p>
    Sempre que uma pessoa é atualizada (<b>created=False</b>) e possui um usuário
    associado, este método sincroniza o nome da pessoa com o campo
    <b>first_name</b> do usuário Django correspondente.
    </p>\n
    """
    if not created and instance.user:
        instance.user.first_name = instance.nome
        instance.user.save()
