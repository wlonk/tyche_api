"""tyche_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from .views import ServerListView, ServerUpdateView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("core.urls")),
    path("accounts/", include("allauth.urls")),
    path("docs/", TemplateView.as_view(template_name="docs.html"), name="docs"),
    path("install/", TemplateView.as_view(template_name="install.html"), name="install"),
    path("about/", TemplateView.as_view(template_name="about.html"), name="about"),
    path("servers/", ServerListView.as_view(), name="server-list"),
    path("server/<int:pk>/", ServerUpdateView.as_view(), name="server-detail"),
    path("", TemplateView.as_view(template_name="root.html"), name="root"),
]
