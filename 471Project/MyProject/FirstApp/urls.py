from django.urls import path
from . import views

urlpatterns = [
    path('FirstApp/', views.FirstView, name='FirstView'),
]