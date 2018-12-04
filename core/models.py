from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField


class User(AbstractUser):
    pass


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


class Server(models.Model):
    PREFIX_CHOICES = (
        ("?", "?"),
        ("!", "!"),
        (":", ":"),
        ("~", "~"),
        ("%", "%"),
    )

    objects = ServerManager()

    server_id = models.CharField(max_length=64, unique=True)
    prefix = models.CharField(max_length=1, choices=PREFIX_CHOICES)
    roles = ArrayField(
        models.CharField(max_length=64),
        blank=True,
        default=list,
    )

    def __str__(self):
        return f"Server({self.server_id!r}, {self.prefix!r})"
