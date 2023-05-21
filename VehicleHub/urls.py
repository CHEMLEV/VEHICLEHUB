from django.urls import path
from . import views

urlpatterns = [
   
    path('join/', views.main_view, name='join'),
    path('register/', views.register_view, name='register'),
]
