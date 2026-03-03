"""Roteamento (URL dispatcher) da aplicação. (core)."""

from django.urls import path

from .views import DashboardView


urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
]
