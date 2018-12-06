from django.shortcuts import render
from django.views import View
import requests

from core.models import Server


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


class ProfileView(View):
    template_name = 'profile.html'

    def get(self, request, *args, **kwargs):
        # This is terrible, making models on a get. This should be in a post login hook!
        discord_servers = get_discord_servers(request.user)
        servers = [
            Server.objects.get_or_create(
                server_id=server["id"],
                defaults=dict(
                    name=server["name"],
                ),
            )[0]
            for server
            in discord_servers
        ]
        return render(request, self.template_name, {'servers': servers})
