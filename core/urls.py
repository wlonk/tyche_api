from django.urls import path
from .views import PrefixView, RoleView


urlpatterns = [
    path("prefix/", PrefixView.as_view()),
    path("roles/", RoleView.as_view()),
]
