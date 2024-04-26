from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import token_obtain_pair

from issues.api import add_new_issue, fetch_issues
from users.api import create_user

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", create_user),
    path("issues/", fetch_issues),
    path("issues/create", add_new_issue),
    path("auth/token/", token_obtain_pair),
    # path("auth/token/", TokenObtainPairView.as_view())
]
