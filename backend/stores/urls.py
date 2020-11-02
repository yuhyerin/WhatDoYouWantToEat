from django.urls import path
from . import views

app_name = 'stores'

urlpatterns = [
    path('input_data/', views.save_stores, name='save_stores'),
    path('store_list/', views.store_list, name='store_list'),
    path('store_category/', views.store_category, name='store_category'),
    path('<int:storeid>/', views.store_detail, name='store_detail'),
    path('add_store/', views.add_store, name='add_store'),
    path('store_bigcategory/', views.store_bigcategory, name='store_bigcategory'),
    # path('review_list/', views.review_list),
]
