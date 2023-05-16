"""
URL configuration for api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework import routers
from . import views

app_name = "cassino"
router = routers.DefaultRouter()
router.register(r"tables", views.TableViewSet, basename="tables")
router.register(r"players", views.PlayerViewSet, basename="players")
router.register(r"transactions", views.TransactionViewSet, basename="transactions")

urlpatterns = router.urls
urlpatterns += staticfiles_urlpatterns()
