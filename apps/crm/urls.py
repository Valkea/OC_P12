""" crm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from .views import (
    ClientViewSet,
    ContractViewSet,
    EventViewSet,
    StatusViewSet,
)

urlpatterns = [
    path(
        "status/",
        StatusViewSet.as_view(
            {
                "get": "list",
            }
        ),
        name="status",
    ),
    path(
        "clients/",
        ClientViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
        name="clients",
    ),
    path(
        "clients/<int:pk>/",
        ClientViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "delete": "destroy",
            }
        ),
        name="client",
    ),
    path(
        "clients/<int:client_pk>/contracts/",
        ContractViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
        name="client_contracts",
    ),
    path(
        "clients/<int:client_pk>/contracts/<int:pk>/",
        ContractViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "delete": "destroy",
            }
        ),
        name="client_contract",
    ),
    path(
        "clients/<int:client_pk>/contracts/<int:contract_pk>/events/",
        EventViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
        name="client_contract_events",
    ),
    path(
        "clients/<int:client_pk>/contracts/<int:contract_pk>/events/<int:pk>/",
        EventViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "delete": "destroy",
            }
        ),
        name="client_contract_event",
    ),
]
