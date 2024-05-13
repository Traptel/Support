from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from issues.api import (
    IssueAPI,
    IssuesRetrieveAPI,
    issues_close,
    issues_take,
    messages_api_dispatcher,
)
from users.api import UserListCreateAPI, UserRetrieveAPI

urlpatterns = [
    # admin
    path("admin/", admin.site.urls),
    # issues
    path("issues/", IssueAPI.as_view()),
    path("issues/<int:id>", IssuesRetrieveAPI.as_view()),
    path("issues/<int:id>/close", issues_close),
    path("issues/<int:id>/take", issues_take),
    # users
    path("users/", UserListCreateAPI.as_view()),
    path("users/<int:id>", UserRetrieveAPI.as_view()),
    # messages
    path("issues/<int:issue_id>/messages", messages_api_dispatcher),
    # Authentication
    path("auth/token/", TokenObtainPairView.as_view()),
    # path("auth/token/", token_obtain_pair),
]
