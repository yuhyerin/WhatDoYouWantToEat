from django.urls import path
from . import views

app_name = 'advertisements'

urlpatterns = [
    path('register_ad/', views.register_ad, name='register_ad'),
    path('find_store/', views.find_store, name='find_store'),
    path('register_ad_info/', views.register_ad_info, name='register_ad_info'),
    path('bizuser_ad_info/', views.bizuser_ad_info, name='bizuser_ad_info'),
    path('ad_to_main/', views.ad_to_main, name='ad_to_main'),
    path('click_ad/', views.click_ad, name='click_ad'),
    path('bizuser_ad_click_info/', views.bizuser_ad_click_info, name='bizuser_ad_click_info'),
]