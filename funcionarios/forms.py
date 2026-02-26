"""Formulários da aplicação. (funcionarios)."""

from django import forms
from .models import Funcionario

# Formulário responsável por validar e organizar os dados desta tela.
class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        exclude = ['data_cadastro']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
            'data_admissao': forms.DateInput(attrs={'type': 'date'}),
        }

    clear_cpf = forms.BooleanField(required=False, label='Limpar CPF')