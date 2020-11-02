from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, UserDetailSerializer, UserProfileSerializer, BizUserProfileSerializer, UserProfileUpdateSerializer
from .serializers import UserOrderSerializer, UserOrderListSerializer
from .models import Order


# 닉네임 중복 여부 체크
@api_view(['POST'])
def user_username(request):
    User = get_user_model()
    try:
        user = User.objects.get(username=request.data.get('username'))
        return Response({'message': '이미 존재하는 닉네임입니다.'})
    except:
        return Response({'message': '사용가능한 닉네임입니다.'})


# 이메일 중복 여부 체크
@api_view(['POST'])
def user_email(request):
    User = get_user_model()
    try:
        user = User.objects.get(email=request.data.get('email'))
        return Response({'message': '이미 존재하는 이메일입니다.'})
    except:
        return Response({'message': '사용가능한 이메일입니다.'})
# res.data.message로 프론트에서 받으면 된다.


@api_view(['POST'])
def email_user_or_bizuser(request):
    User = get_user_model()
    user = User.objects.get(email=request.data.get('email'))
    if user.usertype == 1:
        return Response({'message': 1})
    else:
        return Response({'message': 0})


# user 모델 추가사항들 저장
# 프론트는 headers에 Token 값 담아서 보내야함
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_detail(request):
    serializer = UserDetailSerializer(data=request.data, instance=request.user)
    print(request.data.get('address'))
    if serializer.is_valid(raise_exception=True):
        serializer.save()
    return Response(serializer.data)


# user 프로필 가져오기 or 수정
@api_view(['POST', 'PUT'])
@permission_classes([IsAuthenticated])
def profile(request):
    if request.method == 'POST':
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = UserProfileUpdateSerializer(
            data=request.data, instance=request.user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({'message': '입력한 내용이 올바른지 확인해주세요'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_order_list(request):
    print(request.user)
    order = Order.objects.filter(user=request.user).order_by('-created_at')[:5]
    serializer = UserOrderListSerializer(order, many=True)
    return Response(serializer.data)
    # 아래는 경수님 요청한 데이터 형태로 커스터마이징 했을 경우
    # order_list = {"location": []}
    # for item in order:
    #     order_list["location"].append(item.location)
    # return JsonResponse(order_list)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_order(request):
    serializer = UserOrderSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data)
    else:
        return Response({'message': '입력 내용이 올바른지 확인해주세요'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_nickname(request):
    print("user_nickname 으로 들어왔음 [POST요청]")
    User = get_user_model()
    user = User.objects.get(email=request.user)
    user_nickname = user.username
    return Response({'nickname': user_nickname})
