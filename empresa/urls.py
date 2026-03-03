"""Roteamento (URL dispatcher) da aplicação. (empresa)."""

from django.urls import path
from . import views


urlpatterns = [
    path('', views.EmpresaDetailView.as_view(), name='empresa_detail'),
    path('novo/', views.EmpresaCreateView.as_view(), name='empresa_create'),
    path('editar/', views.EmpresaUpdateView.as_view(), name='empresa_update'),
]
