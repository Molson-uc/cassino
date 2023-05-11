from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import viewsets, status
from django.core.cache import cache
from django_redis import get_redis_connection


class TableViewSet(viewsets.ViewSet):
    def list(self, request):
        db = get_redis_connection("default")
        table_list = db.get
        return Response({"msg": "table list"})

    def create(self, request):
        db = get_redis_connection("default")
        game_master_key = "game_master" + request.data.get("game_master_id")
        game_master_stack = request.data.get("stack") or 0
        table_key = "table" + request.data.get("table_id")
        if db.get(game_master_key) is None:
            db.set(game_master_key, game_master_stack)
        else:
            return Response({"ERROR": "this game master exists"})
        if db.get(table_key) is None:
            db.sadd(table_key, game_master_key)

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
