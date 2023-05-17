from django.urls import path
from . import views

urlpatterns = [
    # Existing URL patterns
    path('main/', views.main_view, name='main'),
]