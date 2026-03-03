"""Configuração do Django Admin para a aplicação. (accounts)."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm


@admin.register(CustomUser)
# Configuração de como este modelo aparece no Django Admin.
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email', 'nome_completo', 'perfil', 'is_active', 'data_cadastro']
    list_filter = ['perfil', 'is_active', 'data_cadastro']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações Pessoais', {'fields': ('nome_completo', 'email')}),
        ('Permissões', {'fields': ('perfil', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas', {'fields': ('last_login', 'date_joined', 'data_cadastro')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('nome_completo', 'username', 'email', 'perfil', 'is_active', 'password1', 'password2'),
        }),
    )

    readonly_fields = ['data_cadastro', 'last_login', 'date_joined']