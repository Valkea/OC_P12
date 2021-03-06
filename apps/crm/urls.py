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
)

urlpatterns = [
    path(
        "clients/",
        ClientViewSet.as_view(
            {
                "get": "list",  # 3
                "post": "create",  # 4
            }
        ),
        name="clients",
    ),
    path(
        "clients/<int:pk>/",
        ClientViewSet.as_view(
            {
                "get": "retrieve",  # 5
                "put": "update",  # 6
                "delete": "destroy",  # 7
            }
        ),
        name="client",
    ),
    path(
        "clients/<int:client_pk>/contracts/",
        ContractViewSet.as_view(
            {
                "get": "list",  # 9
                "post": "create",  # 8
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
                "delete": "destroy",  # 10
            }
        ),
        name="client_contract",
    ),
    # path(
    #     "projects/<int:project_pk>/issues/",
    #     IssueViewSet.as_view(
    #         {
    #             "get": "list",  # 11
    #             "post": "create",  # 12
    #         }
    #     ),
    #     name="project_issues",
    # ),
    # path(
    #     "projects/<int:project_pk>/issues/<int:pk>/",
    #     IssueViewSet.as_view(
    #         {
    #             "get": "retrieve",  # ? pas dans la doc
    #             "put": "update",  # 13
    #             "delete": "destroy",  # 14
    #         }
    #     ),
    #     name="project_issue",
    # ),
    # path(
    #     "projects/<int:project_pk>/issues/<int:issue_pk>/comments/",
    #     CommentViewSet.as_view(
    #         {
    #             "get": "list",  # 16
    #             "post": "create",  # 15
    #         }
    #     ),
    #     name="project_issue_comments",
    # ),
    # path(
    #     "projects/<int:project_pk>/issues/<int:issue_pk>/comments/<int:pk>/",
    #     CommentViewSet.as_view(
    #         {
    #             "get": "retrieve",  # 19
    #             "put": "update",  # 17
    #             "delete": "destroy",  # 18
    #         }
    #     ),
    #     name="project_issue_comment",
    # ),
]
