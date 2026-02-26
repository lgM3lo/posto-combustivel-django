"""Filtros (busca) do app de Funcionários."""

import django_filters
from django.db.models import Q

from .models import Funcionario


# Filtro utilizado para pesquisa e refinamento da listagem.
class FuncionarioFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method="filter_q", label="Pesquisar")

    # ChoiceFilter para permitir "Todos".
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
        model = Funcionario
        fields = ["q", "is_active"]

    def filter_q(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(
            Q(nome_completo__icontains=value)
            | Q(cpf__icontains=value)
            | Q(cargo__icontains=value)
        )

    def filter_is_active(self, queryset, name, value):
        if value == "true":
            return queryset.filter(is_active=True)
        if value == "false":
            return queryset.filter(is_active=False)
        return queryset