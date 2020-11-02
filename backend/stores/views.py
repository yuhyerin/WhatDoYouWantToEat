import json
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Store
from .serializers import StoreSerializer, StoreDetailSerializer
# def save_store(request):
#     # json_data = open('C:\\Users\\multicampus\\Desktop\\dining_data.json').read()
#     json_data = open('stores/dining_data.json').read()
#     json_d = json.loads(json_data)
#     # print(json_d['data'][0]['store_id'])
#     for i in range(10):
#         store = Store()
#         # item = json_d['data'][0][y]
#         # store.storeid = item.get('store_id')
#         # store.category = item.get('category')
#         # store.average_rating = item.get('average_rating')
#         store.storeid = json_d['data'][i]['store_id']
#         store.category = json_d['data'][i]['category']
#         store.average_rating = json_d['data'][0]['average_rating']
#         store.save()
#     return


def save_stores(request):
    json_data = open('stores/bigcategory_stores.json').read()
    json_d = json.loads(json_data)
    for i in range(len(json_d['data'])):
        store = Store()
        store.store_id = json_d['data'][i]['store_id']
        store.store_name = json_d['data'][i]['store_name']
        store.category = json_d['data'][i]['category']
        store.bigcategory = json_d['data'][i]['bigcategory']
        store.address = json_d['data'][i]['address']
        store.latitude = json_d['data'][i]['latitude']
        store.longitude = json_d['data'][i]['longitude']
        store.average_rating = json_d['data'][i]['average_rating']
        store.start_time = json_d['data'][i]['start_time']
        store.end_time = json_d['data'][i]['end_time']
        store.mon = json_d['data'][i]['mon']
        store.tue = json_d['data'][i]['tue']
        store.wed = json_d['data'][i]['wed']
        store.thu = json_d['data'][i]['thu']
        store.fri = json_d['data'][i]['fri']
        store.sat = json_d['data'][i]['sat']
        store.sun = json_d['data'][i]['sun']
        store.min_price = json_d['data'][i]['min_price']
        store.save()
    return Response({'message': 'store데이터 입력 완료'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def store_category(request):
    stores = Store.objects.filter(category=request.data['category'])
    serializer = StoreSerializer(stores, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def store_bigcategory(request):
    # stores = Store.objects.filter(
    #     bigcategory=request.data['bigcategory'], address__contains=request.data['user_location']).order_by('-average_rating')
    # serializer = StoreSerializer(stores, many=True)
    if request.data['bigcategory'] != 'all':
        stores = Store.objects.filter(
            bigcategory=request.data['bigcategory'], address__contains=request.data['user_location']).order_by('-average_rating')
        serializer = StoreSerializer(stores, many=True)
        return Response(serializer.data)
    else:
        stores = Store.objects.filter(
            address__contains=request.data['user_location']).order_by('-average_rating')
        serializer = StoreSerializer(stores, many=True)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def store_list(request):
    if request.user.is_authenticated:
        if request.data['category'] != 'all':
            stores = Store.objects.filter(
                category=request.data['category'], address__contains=request.data['user_location']).order_by('-average_rating')
            serializer = StoreSerializer(stores, many=True)
            return Response(serializer.data)
        else:
            stores = Store.objects.filter(
                address__contains=request.data['user_location']).order_by('-average_rating')
            serializer = StoreSerializer(stores, many=True)
            return Response(serializer.data)
    else:
        return Response({'message': '로그인하세요'})

# Store 상세 정보
# Store에 해당하는 리뷰는 프론트에서 axios 재요청 해야함


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def store_detail(request, storeid):
    # print(request.data['storeid'])
    # storeid = request.data['storeid']
    # store = Store.objects.get(storeid=storeid)
    store = get_object_or_404(Store, store_id=storeid)
    serializer = StoreDetailSerializer(store)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_store(request):
    serializer = StoreSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data)


@api_view(['GET'])
def food_category(request):
    stores = Store.objects.all()
    bigcategory_list = list()
    for store in stores:
        if store.bigcategory in bigcategory_list:
            continue
        else:
            bigcategory_list.append(store.bigcategory)
    return JsonResponse({"bigcategory_list": bigcategory_list})
