"""Modelos (tabelas) da aplicação. (bombas)."""

from django.db import models
from produtos.models import Produto

# Classe do projeto.
class Bomba(models.Model):
    STATUS_CHOICES = (
        ('ATIVA', 'Ativa'),
        ('INATIVA', 'Inativa'),
        ('MANUTENCAO', 'Manutenção'),
    )
    
    numero = models.CharField(max_length=50, unique=True)
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT, related_name='bombas')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='ATIVA')
    localizacao = models.CharField(max_length=100)
    data_instalacao = models.DateField()
    data_ultima_manutencao = models.DateField(blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Bomba {self.numero} - {self.produto.nome}"
