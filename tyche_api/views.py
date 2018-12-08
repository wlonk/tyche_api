from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView

from core.models import Server


class ServerListView(ListView):
    model = Server

    def get_queryset(self):
        return self.model.objects.filter(users=self.request.user)


class ServerUpdateView(UpdateView):
    model = Server
    fields = (
        "prefix",
        "roles",
        "streaming_role",
        "streaming_role_requires",
    )
    template_name_suffix = '_update_form'

    def get_queryset(self):
        return self.model.objects.filter(users=self.request.user)
