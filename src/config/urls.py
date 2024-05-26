from django.contrib import admin
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView

from issues.api import (
    IssueAPI,
    IssuesRetrieveAPI,
    issues_close,
    issues_take,
    messages_api_dispatcher,
)
from users.api import (
    UserListCreateAPI,
    UserRetrieveAPI,
    activate_user,
    resend_activation_user,
)

schema_view = get_schema_view(
    openapi.Info(
        title="Support APi",
        default_version="v1",
        description=(
            "The Backend API that allows you to " "interact with Support Core"
        ),
        contact=openapi.Contact(email="support.support@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

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
    path("users/activate", activate_user),
    path("users/activation/resendActivation", resend_activation_user),
    # messages
    path("issues/<int:issue_id>/messages", messages_api_dispatcher),
    # Authentication
    path("auth/token/", TokenObtainPairView.as_view()),
    # path("auth/token/", token_obtain_pair),
    path(
        "swagger<format>/",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]
