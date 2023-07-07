from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from django_redis import get_redis_connection
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.decorators import permission_required
from .serializers import TableSerializer, PlayerSerializer, TransactionSerializer
from .utils import Transaction
from accounts.permissions import TablesPermission
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes


class TableViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    serializer_class = TableSerializer
    permission_classes = [IsAuthenticated]
    # permission_classes = [TablesPermission]

    def list(self, request):
        print(request.session.items())
        db = get_redis_connection("default")
        table_list = db.keys("table:*")
        return Response({"tables": table_list})

    # @swagger_auto_schema(
    #     request_body=openapi.Schema(
    #         type=openapi.TYPE_OBJECT,
    #         properties={
    #             "table_id": openapi.Schema(type=openapi.TYPE_INTEGER),
    #             "game_master_id": openapi.Schema(type=openapi.TYPE_INTEGER),
    #             "stack": openapi.Schema(type=openapi.TYPE_INTEGER),
    #         },
    #     )
    # )
    @extend_schema(parameters=[TableSerializer], description="create table")
    def create(self, request):
        db = get_redis_connection("default")
        data = JSONParser().parse(request)
        serializer = TableSerializer(data=data)
        game_master_key = ""
        if serializer.is_valid():
            game_master_id = serializer.data.get("game_master_id")
            if db.get(f"game_master:{game_master_id}") is None:
                game_master_key = (
                    f"""game_master:{serializer.data.get("game_master_id")}"""
                )
            else:
                return Response({"error": "this game master is busy"})
            game_master_stack = serializer.data.get("stack") or 0
            table_key = f"""table:{serializer.data.get("table_id")}"""
            db.set(game_master_key, game_master_stack)

            if db.get(table_key) is None:
                db.sadd(table_key, game_master_key)
            else:
                return Response({"ERROR": "this table exists"})

            return Response({"table": "created"})
        return Response({"error": "didnt create new table"})

    @extend_schema(request=TransactionSerializer)
    def update(self, reqeust, pk=None):
        db = get_redis_connection("default")
        player_id = reqeust.data.get("player_id")
        player_key = f"""player:{player_id}"""
        table_key = f"table:{pk}"
        print(player_key, table_key)
        try:
            db.srem(table_key, player_key)
        except Exception as e:
            return Response({"error": e})
        table = db.smembers(table_key)
        print(table)
        return Response({"table": "table"})

    def retrieve(self, request, pk=None):
        db = get_redis_connection("default")
        table = ""
        table = db.smembers(f"""table:{str(pk)}""")
        return Response({f"table{str(pk)}": table})


class PlayerViewSet(viewsets.ViewSet):
    serializer_class = PlayerSerializer

    def list(self, request):
        db = get_redis_connection("default")
        players_list = db.keys("player:*")
        stack_list = [db.get(player) for player in players_list]
        return Response({"players": zip(players_list, stack_list)})

    def create(self, request):
        permission_required = ["accounts.add_table"]
        db = get_redis_connection("default")
        data = JSONParser().parse(request)
        serializer = PlayerSerializer(data=data)
        if serializer.is_valid():
            player_key = f"""player:{serializer.data.get("player_id")}"""
            player_stack = f"""player:{serializer.data.get("stack")}"""
            table_key = f"""table:{serializer.data.get("table_id")}"""
            if db.get(player_key) is None:
                db.set(player_key, player_stack)
                db.sadd(table_key, player_key)
            else:
                return Response({"ERROR": "this player exists"})
        return Response({"player": "created"})

    def retrieve(self, request, pk=None):
        db = get_redis_connection("default")
        player = ""
        try:
            player = db.get(f"player:{str(pk)}")
        except Exception as e:
            return Response({"error": e})
        return Response(player)


class TransactionViewSet(viewsets.ViewSet):
    serializer_class = TransactionSerializer

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "source_id": openapi.Schema(
                    type=openapi.TYPE_STRING, description="player:1"
                ),
                "target_id": openapi.Schema(
                    type=openapi.TYPE_STRING, description="game_master:1"
                ),
                "money": openapi.Schema(type=openapi.TYPE_INTEGER, description="1000"),
            },
        )
    )
    def create(self, request):
        db = get_redis_connection("default")
        data = JSONParser().parse(request)
        table_list = db.keys("table:*")
        serializer = TransactionSerializer(data=data)

        if serializer.is_valid():
            source = serializer.data.get("source_id")
            target = serializer.data.get("target_id")
            money = serializer.data.get("money")
            source_table = ""
            if source == "bank":
                transaction = Transaction()
                try:
                    transaction.recharge_execute(target, money)
                except Exception as e:
                    return Response({"error": e})
                target_stack = db.get(target)
                return Response({"target_stack": target_stack})
            else:
                for table in table_list:
                    if db.sismember(table, source):
                        source_table = table

                if db.sismember(source_table, target):
                    transaction = Transaction()
                    try:
                        transaction.transaction_execute(source, target, money)
                    except Exception as e:
                        return Response({"error": e})
                    source_stack = db.get(source)
                    target_stack = db.get(target)
                    return Response(
                        {"source_stack": source_stack, "target_stack": target_stack}
                    )
        return Response({"error": "player from other table"})
