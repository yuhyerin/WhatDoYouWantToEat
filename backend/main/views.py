from django.shortcuts import render, get_object_or_404
from stores.models import Store
from reviews.models import Review
import json
import pandas as pd
import numpy as np
import os
import pickle5 as pickle
# from lightfm import LightFM

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def recommend_food(request):
    print('들어왔당')
    print(request.user)
    print('위에 머임?')
    User = get_user_model()
    user = User.objects.get(email=request.user)
    user_id = user.id
    print(user_id)
    # user_id = 148970

    embedding_filename = './saved_models/item_embeddings.pickle'
    item_embeddings = pickle.load(open(embedding_filename, 'rb'))

    model_filename = './saved_models/model.pickle'
    model = pickle.load(open(model_filename, 'rb'))

    def make_best_items_report(item_embeddings, src_store_id, num_search_items=10):
        src_idx = Store.objects.get(store_id=src_store_id).id
        print(src_idx)
        # Cosine similarity
        scores = item_embeddings.dot(item_embeddings[src_idx])  # (10000, )
        item_norms = np.linalg.norm(item_embeddings, axis=1)    # (10000, )
        item_norms[item_norms == 0] = 1e-10
        scores /= item_norms

        # best: score가 제일 높은 item의 id를 num_search_items 개 만큼 가져온다.
        best = np.argpartition(scores, -num_search_items)[-num_search_items:]
        similar_item_id_and_scores = sorted(zip(best, scores[best] / item_norms[src_idx]),
                                            key=lambda x: -x[1])
        best_items = pd.DataFrame(
            columns=['store_id', 'category', 'bigcategory'])

        for tar_idx, score in similar_item_id_and_scores:
            # print("tar_idx: ", tar_idx)
            StoreObj = Store.objects.get(id=tar_idx)
            tar_store_id = StoreObj.store_id
            category = StoreObj.category
            bigcategory = StoreObj.bigcategory
            print("tar_store_id: ", tar_store_id, "category: ",
                  category, "bigcategory:", bigcategory)
            row = pd.Series([tar_store_id, category, bigcategory],
                            index=best_items.columns)
            best_items = best_items.append(row, ignore_index=True)

        return best_items

    user_visited_store = Review.objects.filter(userid=user_id)[0].storeid
    print(user_id,"가 갔던 가게 ",user_visited_store," 와 비슷한 가게들")
    report1 = make_best_items_report(item_embeddings, user_visited_store, 5)
    report1 = report1.to_json(orient="split")
    parsed = json.loads(report1)
    return Response(parsed)
    # return Response({'message': '여기요'})
