from django.shortcuts import render
from rest_framework.views import APIView
from .serializer import CustomUserSerializer
from rest_framework.response import Response
from rest_framework import status


class AccountView(APIView):
    def post(self, request, format=None):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
