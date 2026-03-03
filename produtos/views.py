"""Views baseadas em classes (CBVs) da aplicação. (produtos)."""

import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from core.mixins import GerenteRequiredMixin, AuditLogMixin, PaginateBy20Mixin, FlashSuccessMessageMixin, InactivateObjectMixin
from .models import Produto
from .filter import ProdutoFilter
from .services import inativar_produto


audit_logger = logging.getLogger('audit')


# View (CBV) responsável por listar os produtos cadastrados (com paginação e busca).
class ProdutoListView(LoginRequiredMixin, PaginateBy20Mixin, ListView):
    model = Produto
    template_name = 'produtos/produto_list.html'
    context_object_name = 'produtos'
    def get_queryset(self):
        base_qs = Produto.objects.all().order_by('nome')

        # Mantém o comportamento anterior: se o usuário não escolher status,
        # mostramos apenas ativos por padrão.
        data = self.request.GET.copy()
        if not data.get('is_active'):
            data['is_active'] = 'true'

        self.filterset = ProdutoFilter(data=data, queryset=base_qs)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = getattr(self, 'filterset', None)
        return context


# View (CBV) responsável por exibir detalhes de um produto específico.
class ProdutoDetailView(LoginRequiredMixin, DetailView):
    model = Produto
    template_name = 'produtos/produto_detail.html'
    context_object_name = 'produto'


# Mixin reutilizável para compartilhar comportamento entre classes.
class _ProdutoPrecoValidationMixin:
    """Garante RF022: preço de venda não pode ser menor que o preço de custo."""

    def form_valid(self, form):
        preco_custo = form.cleaned_data.get('preco_custo')
        preco_venda = form.cleaned_data.get('preco_venda')
        if preco_custo is not None and preco_venda is not None and preco_venda < preco_custo:
            form.add_error('preco_venda', 'O preço de venda não pode ser menor que o preço de custo.')
            return self.form_invalid(form)
        return super().form_valid(form)


# View (CBV) responsável pelo cadastro (criação) de novos produtos.
class ProdutoCreateView(LoginRequiredMixin, GerenteRequiredMixin, _ProdutoPrecoValidationMixin, AuditLogMixin, FlashSuccessMessageMixin, CreateView):
    audit_action = 'CREATE'
    model = Produto
    fields = ['codigo', 'nome', 'unidade_medida', 'preco_custo', 'preco_venda', 'estoque_atual', 'estoque_minimo', 'is_active']
    template_name = 'produtos/produto_form.html'
    success_url = reverse_lazy('produto_list')

    def perform_inactivation(self, obj, user):
        # delega a regra de inativação para a camada de service
        inativar_produto(obj)

    success_message = 'Produto cadastrado com sucesso!'


# View (CBV) responsável pela edição/atualização de produtos existentes.
class ProdutoUpdateView(LoginRequiredMixin, GerenteRequiredMixin, _ProdutoPrecoValidationMixin, AuditLogMixin, FlashSuccessMessageMixin, UpdateView):
    audit_action = 'UPDATE'
    model = Produto
    fields = ['codigo', 'nome', 'unidade_medida', 'preco_custo', 'preco_venda', 'estoque_atual', 'estoque_minimo', 'is_active']
    template_name = 'produtos/produto_form.html'
    success_url = reverse_lazy('produto_list')

    def perform_inactivation(self, obj, user):
        # delega a regra de inativação para a camada de service
        inativar_produto(obj)

    success_message = 'Produto atualizado com sucesso!'


# View (CBV) responsável por inativar produtos (ajusta campo 'status' para INATIVO).
class ProdutoDeleteView(LoginRequiredMixin, GerenteRequiredMixin, InactivateObjectMixin, DeleteView):
    model = Produto
    success_url = reverse_lazy('produto_list')

    def perform_inactivation(self, obj, user):
        # delega a regra de inativação para a camada de service
        inativar_produto(obj)

    inactivate_field = 'is_active'
    inactivate_value = False
    success_message = 'Produto inativado com sucesso!'