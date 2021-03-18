from django.contrib import admin
from django.urls import path, include
from accounts.views import register
from .views import dash

urlpatterns = [
    path('', dash, name="dashboard"),
]