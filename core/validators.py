"""Validadores reutilizáveis do projeto (ex.: CPF/CNPJ e regras de domínio). (core)."""

import re
from django.core.exceptions import ValidationError


# Função utilitária do projeto.
def validate_cpf(value):
    cpf = re.sub(r"\D", "", str(value))

    if len(cpf) != 11:
        raise ValidationError("CPF deve ter 11 dígitos.")

    # Rejeita sequências do tipo 00000000000
    if cpf == cpf[0] * 11:
        raise ValidationError("CPF inválido.")

    # Validação dos dígitos verificadores (2 últimos dígitos)
    for i in range(9, 11):
        soma = sum(int(cpf[num]) * ((i + 1) - num) for num in range(0, i))
        digito = ((soma * 10) % 11) % 10
        if digito != int(cpf[i]):
            raise ValidationError("CPF inválido.")


# Função utilitária do projeto.
def validate_cnpj(value):
    """
    Valida CNPJ (14 dígitos) com dígitos verificadores.
    Aceita entrada formatada (com . / -) e valida os dois dígitos verificadores.
    """
    cnpj = re.sub(r"\D", "", str(value))

    if len(cnpj) != 14:
        raise ValidationError("CNPJ deve ter 14 dígitos.")

    # Rejeita sequências do tipo 00000000000000
    if cnpj == cnpj[0] * 14:
        raise ValidationError("CNPJ inválido.")

    def calc_dv(base: str) -> str:
        # Pesos oficiais do CNPJ
        pesos_12 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        pesos_13 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        pesos = pesos_12 if len(base) == 12 else pesos_13

        soma = sum(int(d) * p for d, p in zip(base, pesos))
        resto = soma % 11
        dv = 0 if resto < 2 else 11 - resto
        return str(dv)

    dv1 = calc_dv(cnpj[:12])
    dv2 = calc_dv(cnpj[:12] + dv1)

    if cnpj[-2:] != dv1 + dv2:
        raise ValidationError("CNPJ inválido.")
