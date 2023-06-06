from django.urls import path
from . import views
from .views import VehiclesListView, VehicleDetailsView, VehicleCreateView, VehicleUpdateView, VehicleDeleteView



urlpatterns = [
   
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('join/', views.join_view, name='join'),
    path('request_sent.html', views.request_sent_view, name='request_sent'),
    path('ui.html', views.ui_view, name='ui'),
    path('home/', views.HomePageView, name = "home"),
    path("vehicles/", VehiclesListView.as_view(), name = "vehicle_list"),
    path("vehicle/<int:pk>/", VehicleDetailsView.as_view(), name = "vehicle_detail"),
    path("vehicle/new/", VehicleCreateView.as_view(), name = "vehicle_new"),
    path("vehicle/<int:pk>/edit", VehicleUpdateView.as_view(), name = "vehicle_edit" ),
    path("vehicle/<int:pk>/delete", VehicleDeleteView.as_view(), name = "vehicle_delete" ),
    
  
]
