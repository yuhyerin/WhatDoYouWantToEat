from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from stores.models import Store
from stores.serializers import StoreDetailSerializer
from accounts.models import Order
from .models import Advertisement, AdvertisementClick
from .serializers import AdvertisementSerializer, AdvertisementInfoSerializer, AdvertisementClickSerializer, AdvertisementClickInfoSerializer

# 광고 등록시
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_ad(request):
    serializer = AdvertisementSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        # store_id는 가게 이름 검색하면 서버에서 데이터 반환해주므로 꺼낼 수 있다.
        # 여기서 store_id는 store_id의 고유값. 원래부터 갖던 값 아님.
        serializer.save(user=request.user, store_id=request.data["id_store"])
        return Response(serializer.data)
    else:
        return Response({'message': '입력하신 내용을 확인해주세요'})


# 광고 등록시 식당 이름으로 조회할텐데, 이때 이름이 중복될 수 있으므로 해당하는 이름의 가게 목록들 전부 돌려줌
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def find_store(request):
    stores = Store.objects.filter(store_name=request.data["store_name"])
    if len(stores) > 0:
        serializer = StoreDetailSerializer(stores, many=True)
        return Response(serializer.data)
    else:
        return Response({'message': '해당하는 이름의 식당 정보가 없습니다.'})
    


# 광고에 대한 정보 조회시
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_ad_info(request):
    advertisement = Advertisement.objects.get(store_id=request.data["id_store"])
    serializer = AdvertisementInfoSerializer(advertisement)
    return Response(serializer.data)


# 광고주가 자신의 광고 목록 요청할 때 찾아줄 로직 필요
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def bizuser_ad_info(request):
    # 이거로 찾을 필요 없고
    # User = get_user_model()
    # print(request.user)
    # print(request.user.id)
    # bizuser = User.objects.get(email=request.user)

    # 이렇게 찾으면 된다
    advertisement = Advertisement.objects.filter(user=request.user)
    if len(advertisement) > 0:
        serializer = AdvertisementInfoSerializer(advertisement, many=True)
        return Response(serializer.data)
    else:
        return Response({'message': '등록된 광고가 없습니다.'})


# 일반 유저가 로그인하면 메인 페이지로 보낼 광고
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ad_to_main(request):
    User = get_user_model()
    target_user = User.objects.get(email=request.data["email"])
    district = target_user.address.split(" ")

    # 이 부분은 프론트와 상의 필요. 프론트에서 유저의 현재 주소지를 보내줘서 그 주소를 기반으로 광고 지역구와 비교하는건 어떨지
    # (현재 위치는 알 수 없는 상태 => 추천은 유저가 가입할때 등록한 주소 기준? 아니면 최근 주문 기준?)

    # 로그인한 유저의 지역구
    target_user_district = district[1]
    print(target_user_district)
    
    # 광고 지역구와 로그인한 유저의 지역구 일치여부
    stores = Store.objects.filter(address__contains=target_user_district)
    ads = Advertisement.objects.all()
    ad_list = []
    for ad in ads:
        for s in stores:
            if s.id == ad.store_id:
                ad_list.append(ad)
    # if len(ad_list) > 5:
    #     orders = Order.objects.filter(user=request.user).order_by('-created_at')
    #     for order in orders:
    #         order_district = order.location.split(" ")
    #         order_district = order_district[1]
    serializer = AdvertisementInfoSerializer(ad_list, many=True)
    return Response(serializer.data)


# 광고 클릭 정보 쌓을 로직
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def click_ad(request):
    serializer = AdvertisementClickSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user, store_id=request.data["id_store"], advertisement_id=request.data["advertisement_id"])
        return Response({'message': '광고를 클릭하셨습니다'})
    else:
        return Response({'message': '에러'})


# 광고주에게 광고별 클릭 수 반환
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def bizuser_ad_click_info(request):
    stores = Store.objects.filter(user=request.user)

    # serializer = AdvertisementInfoSerializer(stores, many=True)

    clicks = dict()
    for store in stores:
        store_clicks = len(AdvertisementClick.objects.filter(store_id=store.id))
        if store not in clicks:
            clicks[store.store_name] = store_clicks
    return JsonResponse(clicks)
