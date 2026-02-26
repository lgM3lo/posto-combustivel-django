"""Filtros (busca) do app de Produtos.

Objetivo: manter a lógica de pesquisa/filtro fora das CBVs.
As views devem apenas instanciar `ProdutoFilter(request.GET, queryset=...)`
e utilizar `filter.qs`.
"""

import django_filters
from django.db.models import Q

from .models import Produto


# Filtro utilizado para pesquisa e refinamento da listagem.
class ProdutoFilter(django_filters.FilterSet):
    # Campo de busca (nome ou código)
    q = django_filters.CharFilter(method="filter_q", label="Pesquisar")

    # Select com: Todos / Ativo / Inativo (igual aos outros módulos)
    is_active = django_filters.ChoiceFilter(
        choices=(
            ("", "Todos"),
            ("true", "Ativo"),
            ("false", "Inativo"),
        ),
        method="filter_is_active",
        label="Status",
    )

    class Meta:
        model = Produto
        fields = ["q", "is_active"]

    def filter_q(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(Q(nome__icontains=value) | Q(codigo__icontains=value))

    def filter_is_active(self, queryset, name, value):
        if value == "true":
            return queryset.filter(is_active=True)
        if value == "false":
            return queryset.filter(is_active=False)
        return queryset
