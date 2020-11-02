from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Review
from stores.models import Store
from stores.serializers import StoreSerializer
import json
from collections import defaultdict
import re
from .serializers import WholeReviewSerializer, StoreReviewSerializer, ReviewDetailSerializer, ReviewSerializer, ReplySerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

def deEmojify(text):
    regrex_pattern = re.compile(pattern = u'[\U0001f300-\U0001f650]|[\u2000-\u3000]|[\U0001F600-\U0001F64F]|[\U0001F300-\U0001F5FF]|[\U0001F680-\U0001F6FF]|[\U0001F1E0-\U0001F1FF]', flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)

def deEmojify3(text):
    regrex_pattern = re.compile(pattern = u'[\ud800-\udbff][\udc00-\udfff]', flags = re.UNICODE)
    
    return regrex_pattern.sub(r'',text)

def input_data(request):

    f = open(f"reviews/new_reviews_hyerin.json", encoding="UTF-8")
    json_d = json.loads(f.read())

    # json_data = open('reviews/reviews.json').read()
    # json_d = json.loads(json_data)
    for i in range(len(json_d['data'])):
        review = Review()
        review.storeid = json_d['data'][i]['store_id']
        review.userid = json_d['data'][i]['user_id']
        review.score = json_d['data'][i]['score']
        review.reg_time = json_d['data'][i]['reg_time']
        try:
            review.content = deEmojify(json_d['data'][i]['content'])
            review.save()
        except:
            review.content = "맛있어요";
            review.save()
    return Response({'message': 'review데이터 입력 완료'})

# Review 전체
@api_view(['POST'])
def whole_review_list(request):
    reviews = Review.objects.all()
    serializer = WholeReviewSerializer(reviews, many=True)
    return Response(serializer.data)


# 특정 Store에 대한 Review 전체
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def store_review_list(request):
    reviews = Review.objects.filter(storeid=request.data['storeid']).order_by('-pk')
    serializer = ReviewDetailSerializer(reviews, many=True)
    return Response(serializer.data)


# 특정 Review에 대한 자세히 보기
@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def review_detail(request, review_pk):
    if request.method == 'POST':
        review = get_object_or_404(Review, pk=review_pk)
        serializer = ReviewDetailSerializer(review)
        return Response(serializer.data)
    else:
        review = get_object_or_404(Review, pk=review_pk)
        if review.user_id == request.user.id:
            review.delete()
            return Response({'message': '리뷰가 삭제됐습니다'})
        else:
            return Response({'message': '본인이 작성한 글이 아닙니다.'})


# Review 작성
# 작성한 리뷰를 포함한 식당의 리뷰 전체 다시 준다
@api_view(['POST'])
@permission_classes([IsAuthenticated]) # 인증된 사용자의 요청인지 검사하는 데코레이터
def create_review(request):
    serializer = ReviewSerializer(data=request.data)
    print(request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        new_review = Review.objects.filter(storeid=request.data["storeid"]).order_by('-pk')
        serializer = ReviewDetailSerializer(new_review, many=True)

        # 해당 store의 평균 평점 변경
        store = Store.objects.get(store_id=request.data["storeid"])
        dic = {'store_id': store.store_id, 'average_rating': store.average_rating}
        rating = (store.average_rating * len(new_review) + int(request.data["score"]))  // (len(new_review) + 1)
        rating = "%.1f" % rating
        # data로 dictionary 형태가 와야해서 dictionary를 직접 만듬
        store_serializer = StoreSerializer(data=dic, instance=store)
        if store_serializer.is_valid(raise_exception=True):
            store_serializer.save(average_rating=rating)

        return Response(serializer.data)


# 특정 유저의 Review 목록들
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_review_list(request):
    reviews = Review.objects.filter(user=request.user).order_by('-pk')
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_reply(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    store = Store.objects.get(store_id=review.storeid)
    if request.user.id == store.user_id:
        serializer = ReplySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(review_id=review_pk)
            return Response(serializer.data)
    else:
        return Response({'message': '가게 사장님만 등록할 수 있습니다'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def sort_review_latest(request):
    reviews = Review.objects.filter(storeid=request.data['storeid']).order_by('-pk')
    serializer = ReviewDetailSerializer(reviews, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def sort_review_high_score(request):
    reviews = Review.objects.filter(storeid=request.data['storeid']).order_by('-score')
    serializer = ReviewDetailSerializer(reviews, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def sort_review_low_score(request):
    reviews = Review.objects.filter(storeid=request.data['storeid']).order_by('score')
    serializer = ReviewDetailSerializer(reviews, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_reply(request, review_pk, reply_pk):
    print(request.data)
    print(request.data.get("storeid"))
    store = Store.objects.get(store_id=request.data.get("storeid"))
    # print(store.user_id)
    review = Review.objects.get(pk=review_pk)
    replies = review.reply_set.all()
    reply = replies.get(pk=reply_pk)
    print(store.user_id)
    print(request.user.id)
    if request.user.id == store.user_id:
        reply.delete()
        return Response({'message': '답글이 삭제됐습니다.'})
    else:
        return Response({'message': '가게의 사장님만 삭제가능합니다.'})
