from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
class Pessoa(models.Model):
    """
    <h1>Representação da pessoa no banco de dados.</h1>\n
    <h3>Atributos da tabela:</h3> \n
    <b>user (OneToOneField):</b> Associação opcional com o usuário do Django (auth.User).\n
    <b>matricula (CharField):</b> Chave primária da tabela, com até 15 caracteres.\n
    <b>nome (CharField):</b> Tamanho máximo de 100 caracteres, representa o nome completo da pessoa.\n
    <b>must_change_password (BooleanField):</b> Indica se o usuário deve alterar a senha no próximo login.\n
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="pessoa", null=True, blank=True)
    matricula = models.CharField(primary_key=True, max_length=15)
    nome = models.CharField(max_length=100)
    must_change_password = models.BooleanField(default=True)

    @classmethod
    def registrar(cls, matricula, nome, user):
        return cls.objects.create(matricula=matricula, nome=nome, user=user)

    @classmethod
    def partial_search(cls, content):
        """
        <h2>Busca Parcial</h2>\n
        Realiza uma busca não sensitiva utilizando o campo <b>nome</b>.
        """
        return cls.objects.filter(models.Q(nome__icontains=content))
    
    @classmethod
    def getAll(cls):
        return cls.objects.all()
    
    def __str__(self):
        return self.nome
     
class Chave(models.Model):
    """
    <h1>Representação das chaves no banco de dados.</h1>\n
    <h3>Atributos da tabela:</h3> \n
    <b>id (AutoField):</b> Chave primária da tabela.\n
    <b>nome (CharField):</b> Tamanho máximo de 100 caracteres, representa o nome da chave.\n
    Ex:. Laboratório de Informática\n
    <b>itemBusca (CharField):</b> Campo auxiliar utilizado para buscas e exibição em interfaces.
    """
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    itemBusca = models.CharField(max_length=100, blank=True, null=True)

    @classmethod
    def registrar(cls, nome):
        return cls.objects.create(nome=nome)

    @classmethod
    def partial_search(cls, content):
        """
        <h2>Busca Parcial</h2>\n
        Realiza uma busca não sensitiva utilizando o campo <b>itemBusca</b>.
        """
        return cls.objects.filter(models.Q(itemBusca__icontains=content))
    
    @classmethod
    def getAll(cls):
        return cls.objects.all()
    
    def __str__(self):
        return self.nome


class Historico(models.Model):
    """
    <h2>Representação do histórico no banco de dados.</h2>\n
    <h3>Atributos da tabela:</h3> \n
    <b>id_historico (BigAutoField):</b> Chave primária da tabela.\n

    <b>acao (CharField):</b> Representa a ação realizada, limitada às opções definidas em <b>ACAO_CHOICES</b>.\n

    <b>pessoa (ForeignKey):</b> Referência à pessoa responsável pela ação, com exclusão protegida.\n

    <b>chave (ForeignKey):</b> Referência à chave envolvida na ação, com exclusão protegida.\n

    <b>horario (DateTimeField):</b> Data e hora em que a ação foi registrada.
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
        agora = timezone.now()
        return cls.objects.create(acao=acao, pessoa=pessoa, chave=chave, horario=agora)

    def __str__(self):
        return f"{self.acao} - {self.pessoa.nome} - {self.chave.nome}"
    

class ChaveStatus(models.Model):
    """
    <h1>Representação do status atual de uma chave.</h1>\n
    <p>
    Esta tabela representa o estado dinâmico da chave no sistema, indicando
    se está disponível ou em uso, e por quem.
    </p>\n

    <h3>Atributos da tabela:</h3> \n
    <b>chave (OneToOneField):</b> Referência única à chave, também utilizada como chave primária.\n

    <b>pessoa (ForeignKey):</b> Pessoa que está atualmente com a chave. Nulo caso esteja disponível.\n

    <b>checkin (DateTimeField):</b> Data e hora da retirada da chave. Nulo quando a chave está disponível.\n

    <b>status_code (BooleanField):</b> Indica a disponibilidade da chave. 
    <b>True</b> para disponível e <b>False</b> para em uso.
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
        status, created = cls.objects.get_or_create(chave=chave)
        return status

    @classmethod
    def getStatus(cls, pessoa, status_code=None, itemBusca=None, order_by="chave__id"):
        """
        <h2>Buscar Status</h2>\n
        Retorna o status das chaves, aplicando filtros opcionais por disponibilidade
        e por termo de busca. Caso a pessoa possua restrições, apenas as chaves
        permitidas serão retornadas.
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
        Atualiza o status atual de uma chave e registra a operação no histórico.
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
        self.status_code = (self.pessoa is None)
        super().save(*args, **kwargs)


    def __str__(self):
        status = "Disponível" if self.status_code else "Em uso"
        if self.pessoa:
            return f"{self.pessoa.nome} - {self.chave.nome} ({status})"
        return f"{self.chave.nome} ({status})"

class Restricao(models.Model):
    """
    <h2>Restrição de acesso a chaves.</h2>\n
    Define quais chaves uma pessoa está autorizada a acessar.
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
        return Chave.objects.filter(
            permissoes__pessoa=pessoa
        ).distinct()

    class Meta:
        unique_together = ("pessoa", "chave")
        verbose_name = "Permissao de Chave"
        verbose_name_plural = "Permissões de Chaves"

    def __str__(self):
        return f"{self.pessoa.nome} → {self.chave.nome}"