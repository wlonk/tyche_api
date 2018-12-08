from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from allauth.socialaccount.signals import social_account_updated
from django.dispatch import receiver
from django.urls import reverse


import requests


class User(AbstractUser):
    @property
    def servers(self):
        return self.server_set.all()


class ServerManager(models.Manager):
    def prefix_for_id(self, server_id):
        try:
            return self.filter(server_id=server_id).get().prefix
        except (Server.DoesNotExist, Server.MultipleObjectsReturned):
            return "?"

    def roles_for_id(self, server_id):
        try:
            return self.filter(server_id=server_id).get().roles
        except (Server.DoesNotExist, Server.MultipleObjectsReturned):
            return []

    def streaming_role_for_id(self, server_id):
        try:
            server = self.filter(server_id=server_id).get()
            return {
                "streaming_role": server.streaming_role,
                "streaming_role_requires": server.streaming_role_requires,
            }
        except (Server.DoesNotExist, Server.MultipleObjectsReturned):
            return {
                "streaming_role": None,
                "streaming_role_requires": None,
            }


class Server(models.Model):
    PREFIX_CHOICES = (
        ("?", "?"),
        ("!", "!"),
        (":", ":"),
        ("~", "~"),
        ("%", "%"),
    )

    objects = ServerManager()

    name = models.CharField(max_length=1024, blank=True)
    users = models.ManyToManyField(User)
    server_id = models.CharField(max_length=64, unique=True)
    prefix = models.CharField(max_length=1, choices=PREFIX_CHOICES, default="?")
    roles = ArrayField(
        models.CharField(max_length=64),
        blank=True,
        default=list,
    )
    streaming_role = models.CharField(max_length=64, blank=True)
    streaming_role_requires = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return f"Server({self.server_id!r}, {self.prefix!r})"

    def get_absolute_url(self):
        return reverse("server-detail", kwargs={"pk": self.id})


# Signals
def get_discord_servers(user):
    token = user.socialaccount_set.first().socialtoken_set.first().token
    headers = {
        "Authorization": f"Bearer {token}",
    }
    resp = requests.get("https://discordapp.com/api/users/@me/guilds", headers=headers)
    resp.raise_for_status()
    return [
        server
        for server
        in resp.json()
        if server["owner"]
    ]

@receiver(social_account_updated)
def ensure_servers_for_user(request, sociallogin, **kwargs):
    discord_servers = get_discord_servers(request.user)
    for server in discord_servers:
        server, _ = Server.objects.get_or_create(
            server_id=server["id"],
            defaults=dict(
                name=server["name"],
            ),
        )
        server.users.add(request.user)
