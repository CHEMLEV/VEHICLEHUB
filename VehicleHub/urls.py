from django.urls import path
from . import views



urlpatterns = [
   
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('join/', views.join_view, name='join'),
    path('request_sent.html', views.request_sent_view, name='request_sent'),
    path('ui.html', views.ui_view, name='ui'),
    
  
]
