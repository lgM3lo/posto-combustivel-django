"""Configuração do Django Admin para a aplicação. (bombas)."""

from django.contrib import admin

from .models import Bomba


@admin.register(Bomba)
# Configuração de como este modelo aparece no Django Admin.
class BombaAdmin(admin.ModelAdmin):
    list_display = (
        'numero',
        'produto',
        'status',
        'localizacao',
        'data_instalacao',
        'data_ultima_manutencao',
    )
    list_filter = ('status', 'produto', 'localizacao')
    search_fields = ('numero', 'localizacao', 'produto__nome')
    ordering = ('numero',)
