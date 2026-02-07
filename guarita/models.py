from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

class Pessoa(models.Model):
    """
    Representação de uma pessoa no sistema.

    Esta entidade armazena os dados básicos de identificação de usuários
    que interagem com o controle de chaves, podendo ou não estar vinculados
    a uma conta de autenticação do Django.

    Atributos:
        user (OneToOneField):
            Associação opcional com ``django.contrib.auth.models.User``.
            Permite autenticação no sistema.

        matricula (CharField):
            Chave primária da tabela.
            Identificador único da pessoa (máx. 15 caracteres).

        nome (CharField):
            Nome completo da pessoa.
            Máximo de 100 caracteres.

        must_change_password (BooleanField):
            Indica se o usuário deve redefinir a senha no próximo login.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="pessoa", null=True, blank=True)
    matricula = models.CharField(primary_key=True, max_length=15)
    nome = models.CharField(max_length=100)
    must_change_password = models.BooleanField(default=True)

    @classmethod
    def registrar(cls, matricula, nome, user):
        """
        Cria e registra uma nova pessoa no sistema.

        Args:
            matricula (str): Identificador único.
            nome (str): Nome completo.
            user (User): Usuário Django associado.

        Returns:
            Pessoa: Instância criada.
        """
        return cls.objects.create(matricula=matricula, nome=nome, user=user)

    @classmethod
    def partial_search(cls, content):
        """
        Realiza busca parcial por nome.

        A busca é case-insensitive utilizando ``icontains``.

        Args:
            content (str): Texto para busca.

        Returns:
            QuerySet[Pessoa]: Pessoas encontradas.
        """
        return cls.objects.filter(models.Q(nome__icontains=content))
    
    @classmethod
    def getAll(cls):
        """
        Retorna todas as pessoas cadastradas.

        Returns:
            QuerySet[Pessoa]
        """
        return cls.objects.all()
    
    def __str__(self):
        return self.nome
     


class Chave(models.Model):
    """
    Representação das chaves físicas controladas pelo sistema.

    Cada registro corresponde a uma chave real disponível para
    retirada na guarita ou setor responsável.

    Atributos:
        id (AutoField):
            Chave primária.

        nome (CharField):
            Nome identificador da chave.
            Exemplo: "Laboratório de Informática".

        itemBusca (CharField):
            Campo auxiliar utilizado para buscas textuais
            e exibição em interfaces.
            Pode ser nulo ou em branco.
    """
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    itemBusca = models.CharField(max_length=100, blank=True, null=True)

    @classmethod
    def registrar(cls, nome):
        """
        Registra uma nova chave.

        Args:
            nome (str): Nome da chave.

        Returns:
            Chave: Instância criada.
        """
        return cls.objects.create(nome=nome)

    @classmethod
    def partial_search(cls, content):
        """
        Realiza busca parcial pelo campo ``itemBusca``.

        A busca é case-insensitive.

        Args:
            content (str): Texto de busca.

        Returns:
            QuerySet[Chave]
        """
        return cls.objects.filter(models.Q(itemBusca__icontains=content))
    
    @classmethod
    def getAll(cls):
        """
        Retorna todas as chaves cadastradas.

        Returns:
            QuerySet[Chave]
        """
        return cls.objects.all()
    
    def __str__(self):
        return self.nome




class Historico(models.Model):
    """
    Registro histórico de movimentações de chaves.

    Cada operação relevante (retirada, devolução ou atualização)
    gera um registro para auditoria e rastreabilidade.

    Atributos:
        id_historico (BigAutoField):
            Chave primária do histórico.

        acao (CharField):
            Tipo da ação realizada.
            Valores possíveis definidos em ``ACAO_CHOICES``:

                - RETIRADA
                - DEVOLUCAO
                - ATUALIZACAO

        pessoa (ForeignKey):
            Pessoa responsável pela ação.
            Exclusão protegida (PROTECT).

        chave (ForeignKey):
            Chave envolvida na operação.
            Exclusão protegida (PROTECT).

        horario (DateTimeField):
            Data e hora do registro.
    """
    id_historico = models.BigAutoField(primary_key=True)
    
    ACAO_CHOICES = [
        ('RETIRADA', 'Retirada'),
        ('DEVOLUCAO', 'Devolução'),
        ('ATUALIZACAO', 'Atualizacao'),
    ]

    acao = models.CharField(max_length=20, choices=ACAO_CHOICES)

    pessoa = models.ForeignKey(
        Pessoa,
        on_delete=models.PROTECT,
        db_column='Id_pessoa'
    )
    chave = models.ForeignKey(
        Chave,
        on_delete=models.PROTECT,
        db_column='Id_chave'
    )
    horario = models.DateTimeField()

    @classmethod
    def registrar(cls, acao, pessoa, chave):
        """
        Registra automaticamente uma ação no histórico.

        O horário é gerado com ``timezone.now()``.

        Args:
            acao (str): Tipo da ação.
            pessoa (Pessoa): Responsável.
            chave (Chave): Chave envolvida.

        Returns:
            Historico: Registro criado.
        """
        agora = timezone.now()
        return cls.objects.create(acao=acao, pessoa=pessoa, chave=chave, horario=agora)

    def __str__(self):
        return f"{self.acao} - {self.pessoa.nome} - {self.chave.nome}"


class ChaveStatus(models.Model):
    """
    Representa o estado atual de cada chave no sistema.

    Esta tabela mantém o status dinâmico da chave,
    indicando disponibilidade, responsável atual
    e horário da última retirada.

    Atributos:
        chave (OneToOneField):
            Referência única para a chave.
            Também atua como chave primária.

        pessoa (ForeignKey):
            Pessoa que está com a chave no momento.
            Nulo quando disponível.

        checkin (DateTimeField):
            Data e hora da retirada.
            Nulo quando a chave está disponível.

        status_code (BooleanField):
            Código de disponibilidade:

                True  → Disponível
                False → Em uso
    """
    
    chave = models.OneToOneField(
        Chave,
        on_delete=models.PROTECT,
        db_column='Id_chave',
        primary_key=True
    )

    pessoa = models.ForeignKey(
        Pessoa,
        on_delete=models.PROTECT,
        db_column='Id_pessoa',
        null=True,
        blank=True
    )
    
    checkin = models.DateTimeField(null=True, blank=True)
    status_code = models.BooleanField(editable=False)
    
    @classmethod
    def registrar(cls, chave):
        """
        Cria ou recupera o status de uma chave.

        Args:
            chave (Chave)

        Returns:
            ChaveStatus
        """
        status, created = cls.objects.get_or_create(chave=chave)
        return status

    @classmethod
    def getStatus(cls, pessoa, status_code=None, itemBusca=None, order_by="chave__id"):
        """
        Consulta o status das chaves com filtros opcionais.

        Regras aplicadas:

        - Filtra por disponibilidade (status_code).
        - Filtra por termo de busca.
        - Se a pessoa possuir restrições, retorna apenas
          chaves permitidas.

        Args:
            pessoa (Pessoa)
            status_code (bool | None)
            itemBusca (str | None)
            order_by (str)

        Returns:
            QuerySet[ChaveStatus]
        """
        tem_restricao = Restricao.objects.filter(pessoa=pessoa).exists()

        query = cls.objects.select_related("chave", "pessoa")

    
        if tem_restricao:
            query = query.filter(
                chave__permissoes__pessoa=pessoa
            )

        if status_code is not None:
            query = query.filter(status_code=status_code)

        if itemBusca is not None:
            query = query.filter(
                models.Q(chave__itemBusca__icontains=itemBusca) 
            )
            
        return query.distinct().order_by(order_by)

    
    @classmethod
    def update(cls, chave, pessoa, acao):
        """
        Atualiza o status de uma chave e registra no histórico.

        Ações permitidas:

            - RETIRADA
            - DEVOLUCAO

        Validações realizadas:

            - Tipo dos parâmetros.
            - Disponibilidade da chave.
            - Permissões da pessoa.
            - Restrições cadastradas.

        Após atualização, registra automaticamente no histórico.

        Raises:
            ValueError
            TypeError
            PermissionDenied
        """

        #------------------------------VERIFICAR SE AS ENTRADAS SÃO VÁLIDAS---------------------------#
        if acao not in ["RETIRADA", "DEVOLUCAO"]:
            raise ValueError(f"Ação inválida: {acao}. Use 'RETIRADA' ou 'DEVOLUCAO'.")

        if not isinstance(chave, Chave):
            raise TypeError("O parâmetro 'chave' deve ser uma instância válida de Chave.")
        if not isinstance(pessoa, Pessoa):
            raise TypeError("O parâmetro 'pessoa' deve ser uma instância válida de Pessoa.")
        #------------------------------VERIFICAR SE A AÇÃO PODE SER EFETUADA--------------------------#
        status = cls.objects.get(chave=chave)

        if acao == "RETIRADA" and status.pessoa is not None:
            raise ValueError(f"A chave '{status.chave}' já está em uso por {status.pessoa.nome}.")

        if acao == "DEVOLUCAO" and status.pessoa is None:
            raise ValueError(f"A chave '{status.chave}' já está disponível — não há o que devolver.")        
        #------------------------------EFETUAR UPDATE-------------------------------------------------#
        if Restricao.objects.filter(pessoa=pessoa).exists():
            if not Restricao.objects.filter(pessoa=pessoa, chave=chave).exists():
                raise PermissionDenied(
                    f"{pessoa.nome} não tem permissão para acessar a chave {chave.nome}."
        )
        if acao=="DEVOLUCAO":
            status.pessoa = None
            status.checkin = None
            
        else:
            status.pessoa = pessoa
            status.checkin = timezone.now()

        status.save()
        #------------------------------REGISTRAR NO HISTÓRICO-----------------------------------------#
        Historico.registrar(acao, pessoa, chave)

    def save(self, *args, **kwargs):
        """
        Sobrescrita do método save.

        Atualiza automaticamente ``status_code``:

            pessoa is None → Disponível
            pessoa != None → Em uso
        """
        self.status_code = (self.pessoa is None)
        super().save(*args, **kwargs)


    def __str__(self):
        status = "Disponível" if self.status_code else "Em uso"
        if self.pessoa:
            return f"{self.pessoa.nome} - {self.chave.nome} ({status})"
        return f"{self.chave.nome} ({status})"


class Restricao(models.Model):
    """
    Define restrições de acesso a chaves.

    Controla quais pessoas possuem permissão
    para acessar determinadas chaves.

    Atributos:
        pessoa (ForeignKey):
            Pessoa vinculada à permissão.

        chave (ForeignKey):
            Chave permitida para a pessoa.

    Regras:
        - Relação única por par (pessoa, chave).
    """
    pessoa = models.ForeignKey(
        Pessoa,
        on_delete=models.CASCADE,
        related_name="permissoes"
    )

    chave = models.ForeignKey(
        Chave,
        on_delete=models.CASCADE,
        related_name="permissoes"
    )

    @classmethod
    def chaves_permitidas_para_pessoa(cls, pessoa):
        """
        Retorna todas as chaves permitidas para uma pessoa.

        Args:
            pessoa (Pessoa)

        Returns:
            QuerySet[Chave]
        """
        return Chave.objects.filter(
            permissoes__pessoa=pessoa
        ).distinct()

    class Meta:
        """
        Configurações adicionais do modelo.

        unique_together:
            Garante unicidade entre pessoa e chave.

        verbose_name:
            Nome singular administrativo.

        verbose_name_plural:
            Nome plural administrativo.
        """
        unique_together = ("pessoa", "chave")
        verbose_name = "Permissao de Chave"
        verbose_name_plural = "Permissões de Chaves"

    def __str__(self):
        return f"{self.pessoa.nome} → {self.chave.nome}"