from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import viewsets, status
from django.core.cache import cache


@api_view()
def hello(request):
    return HttpResponse("<h1>hello</h1>")


class TodoViewSet(viewsets.ViewSet):
    def get(self, request):
        return Response({"msg": "get"})

    def add(self, request):
        return Response({"msg": "add"})


class TableViewSet(viewsets.ViewSet):
    def list(self, request):
        cache.set("data", "win")

        return Response({"msg": "table list"})

    def create(self, request):
        cache.set("data", "win", version="2")
        print(cache.get("data"))
        try:
            print(request.data.get("msg"))

        except Exception as e:
            print(e)
            return Response({"error": "check content"})
        return Response({"table": "table"})
