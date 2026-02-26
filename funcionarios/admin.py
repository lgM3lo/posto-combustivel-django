"""Configuração do Django Admin para a aplicação. (funcionarios)."""

from django.contrib import admin
from .models import Funcionario

@admin.register(Funcionario)
# Configuração de como este modelo aparece no Django Admin.
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ("nome_completo", "cpf", "cargo", "telefone", "is_active")
    search_fields = ("nome_completo", "cpf", "cargo")
    list_filter = ("cargo", "is_active", "cidade", "estado")
    readonly_fields = ("data_cadastro",)
    ordering = ("nome_completo",)