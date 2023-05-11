from rest_framework import serializers


class TableSerializer(serializers.Serializer):
    table_id = serializers.IntegerField()
    game_master_id = serializers.IntegerField()
