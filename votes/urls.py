from django.urls import path
import votes.views as views

urlpatterns = [
    path('', views.index),
]