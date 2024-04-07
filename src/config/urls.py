from django.contrib import admin
from django.urls import path

from issues.api import add_new_issue, fetch_issues

urlpatterns = [
    path("admin/", admin.site.urls),
    path("issues/", fetch_issues),
    path("issues/create", add_new_issue),
]
