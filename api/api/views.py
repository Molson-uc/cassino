from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import viewsets, status
from django.core.cache import cache
from django_redis import get_redis_connection





class TodoViewSet(viewsets.ViewSet):
    def get(self, request):
        return Response({"msg": "get"})

    def add(self, request):
        return Response({"msg": "add"})


class TableViewSet(viewsets.ViewSet):
    def list(self, request):
        ("data", "win")

        return Response({"msg": "table list"})

    def create(self, request):
        id = 1
        cache.set(f"table:{id}:data", "winnnn", version="")
        cache.
        print(cache.get("table:1:data"))
        try:
            print(request.data.get("msg"))

        except Exception as e:
            print(e)
            return Response({"error": "check content"})
        return Response({"table": "table"})


class PlayerViewSet(viewsets.ViewSet):
    def list(self, request):
        cache.get("player")
        return Response({"player": "list"})

    def create(self, request):
        return Response({"player": "create"})

    def get(self, request):
        return Response({"player": "get"})


class TransactionViewSet(viewsets.ViewSet):
    pass
