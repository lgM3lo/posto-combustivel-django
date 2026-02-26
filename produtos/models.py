"""Modelos (tabelas) da aplicação. (produtos)."""

from django.db import models
from django.core.exceptions import ValidationError

# Classe do projeto.
class Produto(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nome = models.CharField(max_length=100)
    unidade_medida = models.CharField(max_length=20, default='Litros')
    preco_custo = models.DecimalField(max_digits=10, decimal_places=2)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2)
    estoque_atual = models.DecimalField(max_digits=10, decimal_places=2)
    estoque_minimo = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.preco_venda < self.preco_custo:
            raise ValidationError('O preço de venda não pode ser menor que o preço de custo.')

    def __str__(self):
        return self.nome
