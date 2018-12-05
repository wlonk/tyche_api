from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Server


class PrefixView(APIView):
    def get(self, request):
        return Response({
            "prefix": Server.objects.prefix_for_id(
                request.query_params.get("server_id", ""),
            ),
        })


class RoleView(APIView):
    def get(self, request):
        return Response({
            "roles": Server.objects.roles_for_id(
                request.query_params.get("server_id", ""),
            ),
        })


class StreamingRoleView(APIView):
    def get(self, request):
        return Response(
            Server.objects.streaming_role_for_id(
                request.query_params.get("server_id", ""),
            ),
        )
