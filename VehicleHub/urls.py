from django.urls import path
from . import views
from .views import VehiclesListView, VehicleDetailsView, VehicleCreateView, VehicleUpdateView, VehicleDeleteView



urlpatterns = [
   
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('join/', views.join_view, name='join'),
    path('request_sent', views.request_sent_view, name='request_sent'),
    path('ui', views.ui_view, name='ui'),
    path('manage_records', views.manage_records_view, name='manage_records'),
    path('add_record_types', views.add_record_types_view, name='add_record_types'),
    path('search_edit_record_types', views.search_edit_record_types_view, name='search_edit_record_types'),
    path('home/', views.HomePageView, name = "home"),
    path("request_report/", VehiclesListView.as_view(), name = "request_report"),
    path("report_details/<int:pk>/", VehicleDetailsView.as_view(), name = "report_details"),
    path("vehicle/<int:pk>/", VehicleDetailsView.as_view(), name = "vehicle_detail"),
    path("vehicle/new/", VehicleCreateView.as_view(), name = "vehicle_new"),
    path("vehicle/<int:pk>/edit", VehicleUpdateView.as_view(), name = "vehicle_edit" ),
    path("vehicle/<int:pk>/delete", VehicleDeleteView.as_view(), name = "vehicle_delete" ),
    
  
]
