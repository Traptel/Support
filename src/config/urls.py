from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from issues.api import IssueAPI, IssuesRetrieveAPI
from users.api import UserListCreateAPI, UserRetrieveAPI

urlpatterns = [
    path("admin/", admin.site.urls),
    path("issues/", IssueAPI.as_view()),
    path("issues/<int:id>", IssuesRetrieveAPI.as_view()),
    path("users/", UserListCreateAPI.as_view()),
    path("users/<int:id>", UserRetrieveAPI.as_view()),
    path("auth/token/", TokenObtainPairView.as_view()),
    # path("auth/token/", token_obtain_pair),
]
