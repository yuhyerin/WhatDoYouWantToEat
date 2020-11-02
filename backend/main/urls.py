from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    # path('<int:store_pk>/', views.get_stores, name='get_stores'),
    path('', views.recommend_food, name='recommend_food'),
]