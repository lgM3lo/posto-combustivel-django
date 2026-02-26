"""Views baseadas em classes (CBVs) da aplicação. (core)."""

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from produtos.models import Produto
from bombas.models import Bomba
from funcionarios.models import Funcionario

# View (CBV) responsável por montar e exibir o painel principal (dashboard) do sistema.
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'core/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_produtos'] = Produto.objects.count()
        context['total_bombas'] = Bomba.objects.count()
        context['total_funcionarios'] = Funcionario.objects.count()
        context['estoque_baixo'] = Produto.objects.filter(estoque_atual__lte=models.F('estoque_minimo')).count()
        return context