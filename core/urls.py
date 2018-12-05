from django.urls import path
from .views import PrefixView, RoleView, StreamingRoleView


urlpatterns = [
    path("prefix/", PrefixView.as_view()),
    path("roles/", RoleView.as_view()),
    path("streaming_role/", StreamingRoleView.as_view()),
]
