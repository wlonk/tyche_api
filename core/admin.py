from django.contrib import admin

from .models import User, Server


admin.site.register(User)
admin.site.register(Server)
