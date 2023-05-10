from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view()
def hello(request):
    return HttpResponse("<h1>hello</h1>")
