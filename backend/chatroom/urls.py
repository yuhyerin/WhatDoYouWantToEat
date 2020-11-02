from django.urls import path

from . import views

app_name = 'chatroom'

urlpatterns = [

    path('createchatroom/', views.create_chatroom, name='makechatroom'),
    path('store_chatroom_list/', views.store_chatroom_list,
         name='store_chatroom_list'),
]
