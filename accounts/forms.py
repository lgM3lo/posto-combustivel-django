"""Formulários da aplicação. (accounts)."""

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

# Formulário responsável por validar e organizar os dados desta tela.
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('nome_completo', 'username', 'email', 'perfil', 'is_active')

# Formulário responsável por validar e organizar os dados desta tela.
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('nome_completo', 'username', 'email', 'perfil', 'is_active')
