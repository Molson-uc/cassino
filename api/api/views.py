from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import viewsets, status
from django.core.cache import cache
from rest_framework.parsers import JSONParser
from django_redis import get_redis_connection
from .serializers import TableSerializer


class TableViewSet(viewsets.ViewSet):
    def list(self, request):
        db = get_redis_connection("default")
        table_list = db.keys("table:*")
        table_values = db.mget(table_list)
        return Response({"tables": zip(table_list, table_values)})

    def create(self, request):
        db = get_redis_connection("default")
        data = JSONParser().parse(request)
        serializer = TableSerializer(data=data)
        if serializer.is_valid():
            game_master_key = f"""game_master:{serializer.data.get("game_master_id")}"""
            game_master_stack = serializer.data.get("stack") or 0
            table_key = f"""table:{serializer.data.get("table_id")}"""

            if db.get(game_master_key) is None:
                db.set(game_master_key, game_master_stack)
            else:
                return Response({"ERROR": "this game master exists"})
            if db.get(table_key) is None:
                db.sadd(table_key, game_master_key)
            else:
                return Response({"ERROR": "this table exists"})

        return Response({"table": "create"})


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
