"""Roteamento (URL dispatcher) da aplicação. (funcionarios)."""

from django.urls import path
from . import views


urlpatterns = [
    # Rotas recomendadas (padrão do sistema)
    path('', views.FuncionarioListView.as_view(), name='funcionario_list'),
    path('<int:pk>/', views.FuncionarioDetailView.as_view(), name='funcionario_detail'),
    path('novo/', views.FuncionarioCreateView.as_view(), name='funcionario_create'),
    path('<int:pk>/editar/', views.FuncionarioUpdateView.as_view(), name='funcionario_update'),
    path('<int:pk>/deletar/', views.FuncionarioDeleteView.as_view(), name='funcionario_delete'),

    # Rotas "legadas" (mantidas por compatibilidade / referência)
    path('_legacy/', views.FuncionarioListView.as_view(), name='index'),
    path('_legacy/tabela/', views.FuncionarioListView.as_view(), name='table'),
    path('_legacy/incluir/', views.FuncionarioCreateView.as_view(), name='create'),
    path('_legacy/atualizar/<int:pk>/', views.FuncionarioUpdateView.as_view(), name='update'),
    path('_legacy/excluir/<int:pk>/', views.FuncionarioDeleteView.as_view(), name='delete'),
]
