from django.shortcuts import render, get_object_or_404
from stores.models import Store
from reviews.models import Review
from rest_framework.response import Response
from rest_framework.decorators import api_view

# 기본라이브러리 
import pandas as pd
import numpy as np

# 데이터셋 
from lightfm.data import Dataset

# 교차검증 
from lightfm.cross_validation import random_train_test_split

# lightfm 
from hyperopt import fmin, hp, tpe, Trials
from lightfm import LightFM
from lightfm.evaluation import precision_at_k

# 파일 입출력 
import os
import pickle

# Create your views here.
@api_view(['GET'])
def calc(request):
    try :
        stores =  Store.objects.all();
        reviews = Review.objects.all();

        stores = pd.DataFrame(list(stores.values('id', 'store_id','store_name', 'category',
        'address','latitude','longitude','average_rating')))
        reviews = pd.DataFrame(list(reviews.values('id', 'storeid','userid', 'score','reg_time')))

        reviews_source = [(reviews['userid'][i], reviews['storeid'][i]) for i in range(reviews.shape[0])]
        item_feature_source = [(stores['store_id'][i], [ stores['category'][i],stores['address'][i],stores['latitude'][i],stores['longitude'][i], stores['average_rating'][i]] ) for i in range(stores.shape[0]) ]

        dataset = Dataset()
        dataset.fit(users=reviews['userid'].unique(),
            items=reviews['storeid'].unique(),
            item_features=stores[stores.columns[1:]].values.flatten())

        interactions, weights = dataset.build_interactions(reviews_source)
        item_features = dataset.build_item_features(item_feature_source)

        # Split Train, Test data
        train, test = random_train_test_split(interactions, test_percentage=0.1)
        train, test = train.tocsr().tocoo(), test.tocsr().tocoo()
        train_weights = train.multiply(weights).tocoo()

        # Define Search Space
        trials = Trials()
        space = [hp.choice('no_components', range(10, 50, 10)), hp.uniform('learning_rate', 0.01, 0.05)]

        # Define Objective Function
        def objective(params):
            no_components, learning_rate = params
            global model
            model = LightFM(no_components=no_components,
                            learning_schedule='adagrad',
                            loss='warp',
                            learning_rate=learning_rate,
                            random_state=0)

            model.fit(interactions=train,
                    item_features=item_features,
                    sample_weight=train_weights,
                    epochs=3,
                    verbose=False)

            test_precision = precision_at_k(model, test, k=5, item_features=item_features).mean()
            print("no_comp: {}, lrn_rate: {:.5f}, precision: {:.5f}".format(
            no_components, learning_rate, test_precision))
            # test_auc = auc_score(model, test, item_features=item_features).mean()
            output = -test_precision

            if np.abs(output+1) < 0.01 or output < -1.0:
                output = 0.0

            return output

        # max_evals가 몇번 반복실행 할껀지. 
        best_params = fmin(fn=objective, space=space, algo=tpe.suggest, max_evals=10, trials=trials)

        # 아이템피쳐 저장        
        with open('./saved_models/item_features.pickle', 'wb') as fle:
            pickle.dump(item_features, fle, protocol=pickle.HIGHEST_PROTOCOL)

        # 모델 저장해야 됨
        with open('./saved_models/model.pickle', 'wb') as fle:
            pickle.dump(model, fle, protocol=pickle.HIGHEST_PROTOCOL)

        item_biases, item_embeddings = model.get_item_representations(features=item_features)
        # item_embeddings 저장하기 
        with open('./saved_models/item_embeddings.pickle', 'wb') as fle:
            pickle.dump(item_embeddings, fle, protocol=pickle.HIGHEST_PROTOCOL)
        
        return Response({'result': True}) 
    
    except :
        return Response({'result': False}) 