"""Roteamento (URL dispatcher) da aplicação. (bombas)."""

from django.urls import path
from . import views


urlpatterns = [
    path('', views.BombaListView.as_view(), name='bomba_list'),
    path('<int:pk>/', views.BombaDetailView.as_view(), name='bomba_detail'),
    path('novo/', views.BombaCreateView.as_view(), name='bomba_create'),
    path('<int:pk>/editar/', views.BombaUpdateView.as_view(), name='bomba_update'),
    path('<int:pk>/deletar/', views.BombaDeleteView.as_view(), name='bomba_delete'),
]
