from django.contrib import admin
from django.urls import path
from attendance import views

urlpatterns = [
    path('',views.index, name='attendance')
]