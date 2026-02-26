"""Testes automatizados da aplicação. (core)."""

from datetime import date

from django.core.exceptions import ValidationError
from django.test import TestCase

from accounts.models import CustomUser
from empresa.models import Empresa
from funcionarios.models import Funcionario
from produtos.models import Produto


# Classe do projeto.
class AuthRequirementTests(TestCase):
    """Requisitos de autenticação e segurança (RF006/RNF006)."""

    def test_inactive_user_cannot_login(self):
        # Usuário inativo não deve conseguir autenticar.
        # Usamos client.login() para evitar renderização de templates durante o teste
        # (mais estável e suficiente para validar a regra).
        CustomUser.objects.create_user(
            username='operador_inativo',
            password='SenhaTeste123',
            email='operador_inativo@example.com',
            nome_completo='Operador Inativo',
            perfil='OPERADOR',
            is_active=False,
        )

        logged_in = self.client.login(username='operador_inativo', password='SenhaTeste123')
        self.assertFalse(logged_in)
# Classe do projeto.
class BusinessValidationTests(TestCase):
    """Validações de negócio (RF022, RF014, RF030)."""

    def test_produto_preco_venda_nao_pode_ser_menor_que_preco_custo(self):
        produto = Produto(
            codigo='GAS001',
            nome='Gasolina Comum',
            unidade_medida='Litros',
            preco_custo='5.00',
            preco_venda='4.99',
            estoque_atual='100.00',
            estoque_minimo='10.00',
            is_active=True,
        )
        with self.assertRaises(ValidationError):
            produto.full_clean()

    def test_empresa_cnpj_invalido_dispara_validation_error(self):
        empresa = Empresa(
            razao_social='Empresa Teste LTDA',
            nome_fantasia='Posto Teste',
            cnpj='00.000.000/0000-00',  # inválido
            inscricao_estadual='ISENTO',
            telefone='(00) 0000-0000',
            email='contato@teste.com',
            cep='00000-000',
            logradouro='Rua Teste',
            numero='123',
            complemento='',
            bairro='Centro',
            cidade='Cidade',
            estado='CE',
        )
        with self.assertRaises(ValidationError):
            empresa.full_clean()

    def test_funcionario_cpf_invalido_dispara_validation_error(self):
        funcionario = Funcionario(
            nome_completo='Fulano de Tal',
            cpf='000.000.000-00',  # inválido
            rg='123456',
            data_nascimento=date(2000, 1, 1),
            telefone='(00) 00000-0000',
            email='fulano@teste.com',
            cep='00000-000',
            logradouro='Rua Teste',
            numero='10',
            complemento='',
            bairro='Centro',
            cidade='Cidade',
            estado='CE',
            cargo='Frentista',
            data_admissao=date(2020, 1, 1),
            salario='1500.00',
            is_active=True,
        )
        with self.assertRaises(ValidationError):
            funcionario.full_clean()
