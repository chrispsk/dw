from django.contrib import admin
from django.urls import path, include
from accounts.views import register
from .views import dash, graph2, graph3, fake

urlpatterns = [
    path('', fake, name="fake"),
    path('graph1/', dash, name="dashboard"),
    path('graph2/', graph2, name="graph2"),
    path('graph3/', graph3, name="graph3"),
]