from django.shortcuts import render
from django.contrib.auth import get_user_model
from .serializers import ChatRoomSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import makeChatroom

@api_view(['POST'])
def create_chatroom(request):  # 채팅방 생성

    serializer = ChatRoomSerializer(data=request.data)

    # store_id 꺼내고
    store_id = request.data["store_id"]
    # user_id 꺼내서
    User = get_user_model()
    user = User.objects.get(email=request.user)
    user_id = user.id
    print(user_id)
    key = str(store_id) + "_" + str(user_id)
    print(key)

    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)

    return Response({"key": key})


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def store_chatroom_list(request):
    rooms = makeChatroom.objects.filter(store_id=request.data['store_id'])
    if request.method == 'POST':
        if len(rooms) > 0:
            serializer = ChatRoomSerializer(rooms, many=True)
            return Response(serializer.data)
        else:
            return Response({'message': '해당 식당의 채팅방이 존재하지 않습니다.'})
    else:
        room = makeChatroom.objects.get(user=request.user)
        try:
            room.delete()
            return Response({'message': '채팅방이 삭제되었습니다.'})
        except:
            return Response({'message': '본인이 만든 방이 아닙니다.'})


def user_minuscount(request, store_info, user_info):
    chatroom = makeChatroom.objects.get(store_id=store_info)
    cnt = chatroom.usercount - 1
    print("현재 참여자 수 ", cnt)
    chatroom.usercount = cnt
    chatroom.save()
    return chatroom.usercount


def user_pluscount(request, store_info, user_info):
    chatroom = makeChatroom.objects.get(store_id=store_info)
    print(chatroom)
    cnt = chatroom.usercount + 1
    print("현재 참여자 수 ", cnt)
    chatroom.usercount = cnt
    chatroom.save()
    return chatroom.usercount


def delete_chatroom(request, store_info, user_info):
    room = makeChatroom.objects.get(store_id=store_info, user=user_info)
    room.delete()
    print("delete_chatroom: 방삭제")
