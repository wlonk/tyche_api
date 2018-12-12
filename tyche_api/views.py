from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView

from core.models import Server
from core.forms import ServerForm


class ServerListView(ListView):
    model = Server

    def get_queryset(self):
        return self.model.objects.filter(users=self.request.user)


class ServerUpdateView(UpdateView):
    model = Server
    template_name_suffix = '_update_form'
    form_class = ServerForm

    def get_queryset(self):
        return self.model.objects.filter(users=self.request.user)
