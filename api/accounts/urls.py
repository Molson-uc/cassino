from django.contrib import admin
from django.urls import include, re_path, path
from .views import AccountView


urlpatterns = [path("", AccountView.as_view())]
