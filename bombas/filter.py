"""Filtros (busca) do app de Bombas.

Requisito: permitir filtrar por status e produto (e opcionalmente por número).
"""

import django_filters
from django.db.models import Q

from produtos.models import Produto

from .models import Bomba


# Filtro utilizado para pesquisa e refinamento da listagem.
class BombaFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method="filter_q", label="Pesquisar")

    status = django_filters.ChoiceFilter(
        choices=(("", "Todos"),) + Bomba.STATUS_CHOICES,
        field_name="status",
        label="Status",
    )

    produto = django_filters.ModelChoiceFilter(
        queryset=Produto.objects.all().order_by("nome"),
        field_name="produto",
        empty_label="Todos",
        label="Produto",
    )

    class Meta:
        model = Bomba
        fields = ["q", "status", "produto"]

    def filter_q(self, queryset, name, value):
        if not value:
            return queryset
        # Busca pelo número e também pelo nome do produto.
        return queryset.filter(Q(numero__icontains=value) | Q(produto__nome__icontains=value))
