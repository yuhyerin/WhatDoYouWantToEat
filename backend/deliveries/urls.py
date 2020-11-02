from django.urls import path
from . import views

app_name = 'deliveries'

urlpatterns = [
    path('input_data/', views.save_delivery)
]