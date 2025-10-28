from django.db import models

class Pessoa(models.Model):
    matricula = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nome} ({self.cargo})"


class Chave(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Historico(models.Model):
    id_historico = models.AutoField(primary_key=True)
    
    ACAO_CHOICES = [
        ('RETIRADA', 'Retirada'),
        ('DEVOLUCAO', 'Devolução'),
        ('ATUALIZACAO', 'Atualizacao'),
    ]

    acao = models.CharField(max_length=20, choices=ACAO_CHOICES)

    id_pessoa = models.ForeignKey(
        Pessoa,
        on_delete=models.PROTECT,
        db_column='Id_pessoa'
    )
    id_chave = models.ForeignKey(
        Chave,
        on_delete=models.PROTECT,
        db_column='Id_chave'
    )
    horario = models.DateTimeField()

    def __str__(self):
        return f"{self.acao} - {self.id_pessoa.nome} - {self.id_chave.nome}"


class ChaveStatus(models.Model):
    id_chave = models.OneToOneField(
        Chave,
        on_delete=models.PROTECT,
        db_column='Id_chave',
        primary_key=True
    )

    id_pessoa = models.ForeignKey(
        Pessoa,
        on_delete=models.PROTECT,
        db_column='Id_pessoa'
    )
    
    checkin = models.DateTimeField()
    status_code = models.BooleanField()

    class Meta:
        # Opcional: evita duplicar combinações pessoa/chave
        unique_together = ('id_pessoa', 'id_chave')

    def __str__(self):
        status = "Ativo" if self.status_code else "Inativo"
        return f"{self.id_pessoa.nome} - {self.id_chave.nome} ({status})"
