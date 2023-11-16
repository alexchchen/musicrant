from django.urls import path
from . import views

urlpatterns = [
    path('FirstApp/', views.FirstView, name='FirstView'),
    path('', views.homePage, name='homePage'),
    path('FirstApp/profile/<username>', views.profile, name='profile')
]