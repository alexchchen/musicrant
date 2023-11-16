from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('FirstApp/', views.FirstView, name='FirstView'),
    path('FirstApp/profile/<username>', views.profile, name='profile')
]