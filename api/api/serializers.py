from rest_framework import serializers


class TableSerializer(serializers.Serializer):
    table_id = serializers.IntegerField()
    game_master_id = serializers.IntegerField()


class PlayerSerializer(serializers.Serializer):
    player_id = serializers.IntegerField()
    stack = serializers.IntegerField()


class TransactionSerializer(serializers.Serializer):
    source_id = serializers.CharField(max_length=50)
    target_id = serializers.CharField(max_length=50)
    money = serializers.IntegerField()
