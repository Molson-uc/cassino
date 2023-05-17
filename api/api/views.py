from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets

from rest_framework.parsers import JSONParser
from django_redis import get_redis_connection
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .serializers import TableSerializer, PlayerSerializer, TransactionSerializer
from .transactions import Transation


class TableViewSet(viewsets.ViewSet):
    serializer_class = TableSerializer

    def list(self, request):
        db = get_redis_connection("default")
        table_list = db.keys("table:*")
        table_urls = [
            f"""http://127.0.0.1:8000/tables/{str(id[6:],"utf-8")}/"""
            for id in table_list
        ]
        return Response({"tables": zip(table_list, table_urls)})

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "table_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="example: 11"
                ),
                "game_master_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="example: 11"
                ),
                "stack": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="example: 0"
                ),
            },
        )
    )
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

        return Response({"table": "created"})

    def retrieve(self, request, pk=None):
        db = get_redis_connection("default")

        table = ""
        try:
            table = db.smembers(f"""table:{str(pk)}""")
        except Exception as e:
            print(e)
            return Response({"error": "error"})

        return Response({f"table{str(pk)}": table})


class PlayerViewSet(viewsets.ViewSet):
    serializer_class = PlayerSerializer

    def list(self, request):
        db = get_redis_connection("default")
        player_list = db.keys("player:*")

        player_urls = [
            f"""http://127.0.0.1:8000/players/{str(id[7:],"utf-8")}/"""
            for id in player_list
        ]
        return Response({"players": zip(player_list, player_urls)})

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "player_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="example: 11"
                ),
                "stack": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="example: 10000"
                ),
            },
        )
    )
    def create(self, request):
        db = get_redis_connection("default")
        data = JSONParser().parse(request)
        serializer = PlayerSerializer(data=data)
        if serializer.is_valid():
            player_key = f"""player:{serializer.data.get("player_id")}"""
            player_stack = f"""player:{serializer.data.get("stack")}"""
            if db.get(player_key) is None:
                db.set(player_key, player_stack)
            else:
                return Response({"ERROR": "this player exists"})

        return Response({"player": "create"})

    def get(self, request):
        return Response({"player": "get"})

    def retrieve(self, request, pk=None):
        db = get_redis_connection("default")
        player = ""
        try:
            player = db.get(f"player:{str(pk)}")
        except Exception as e:
            print(e)
            return Response({"error": e})

        return Response({"stack": player})


class TransactionViewSet(viewsets.ViewSet):
    serializer_class = TransactionSerializer

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "source_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="example: player:1"
                ),
                "target_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="example: player:2"
                ),
                "money": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="example: 1000"
                ),
            },
        )
    )
    def create(self, request):
        db = get_redis_connection("default")
        data = JSONParser().parse(request)
        serializer = TransactionSerializer(data=data)
        if serializer.is_valid():
            source = serializer.data.get("source_id")
            target = serializer.data.get("target_id")
            money = serializer.data.get("money")
            transaction = Transation()
            try:
                transaction.transaction(source, target, money)
            except Exception as e:
                print(e)
                return Response({"error": "error"})
            source_stack = db.get(source)
            target_stack = db.get(target)
            return Response(
                {"source_stack": source_stack, "target_stack": target_stack}
            )
        return Response({"error": "error"})
