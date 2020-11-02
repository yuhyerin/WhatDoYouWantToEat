from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('input_data/', views.input_data),
    path('whole_review_list/', views.whole_review_list),
    path('store_review_list/', views.store_review_list),
    path('<int:review_pk>/', views.review_detail),
    path('create_review/', views.create_review),
    path('user_review_list/', views.user_review_list),
    path('<int:review_pk>/create_reply/', views.create_reply),
    path('sort_review_latest/', views.sort_review_latest),
    path('sort_review_high_score/', views.sort_review_high_score),
    path('sort_review_low_score/', views.sort_review_low_score),
    path('<int:review_pk>/reply/<int:reply_pk>/', views.remove_reply),
]