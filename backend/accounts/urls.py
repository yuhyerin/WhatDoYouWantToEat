from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('user_username/', views.user_username, name='user_usernmae'),
    path('user_email/', views.user_email, name='user_email'),
    path('email_user_or_bizuser/', views.email_user_or_bizuser,
         name='email_user_or_bizuser'),
    path('user_detail/', views.user_detail, name='user_detail'),
    path('profile/', views.profile, name='profile'),
    path('user_order_list/', views.user_order_list, name='user_order_list'),
    path('user_order/', views.user_order, name='user_order'),
    path('user_nickname/', views.user_nickname, name="user_nickname"),
]
