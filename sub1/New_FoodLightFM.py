import json
import pandas as pd
import numpy as np
import os
import shutil
import pickle
from lightfm.data import Dataset
from scipy.io import mmwrite
from lightfm.cross_validation import random_train_test_split
from hyperopt import fmin, hp, tpe, Trials
from lightfm import LightFM
from lightfm.evaluation import precision_at_k

DATA_DIR = "../data"
DATA_FILE = os.path.join(DATA_DIR, "data.json")
DINING_DATA_FILE = os.path.join(DATA_DIR, "dining_data.json")
DUMP_FILE = os.path.join(DATA_DIR, "dump.pkl")

# 데이터 불러들이는 함수1
def import_diningdata(data_path=DINING_DATA_FILE):
    
    try:
        with open(data_path, encoding="utf-8") as f:
            data = json.loads(f.read())
    except FileNotFoundError as e:
        print(f"`{data_path}` 가 존재하지 않습니다.")
        exit(1)

    data = data["data"]
    stores = []  # 음식점 테이블
    

    for d in data:
        
        stores.append(
            [
                d["store_id"],
                d["category"],
                d["average_rating"],
            ]
        )

    store_frame = pd.DataFrame(data=stores, columns=("store_id", "category","average_rating"))

    return { "stores": store_frame }

def import_data(data_path=DATA_FILE):
    
    try:
        with open(data_path, encoding="utf-8") as f:
            data = json.loads(f.read())
    except FileNotFoundError as e:
        print(f"`{data_path}` 가 존재하지 않습니다.")
        exit(1)

    all_stores = [] # 모든 가게 테이블
    reviews = []  # 리뷰 테이블
    for d in data:
        
        
        for c in d["category_list"]:
            category = c["category"] # 대분류 카테고리만 사용하겠음. 
            break
            
        all_stores.append(
            [
                d["id"],
                d["name"],
                category,
            ]
        )
            
        
        for review in d["review_list"]:
            r = review["review_info"]
            u = review["writer_info"]

            reviews.append(
                [d["id"], u["id"], r["score"]]
            )
    
    # 식당ID, 식당명, category
    store_frame = pd.DataFrame(data=all_stores, columns=("store_id", "store_name","category"))
    
    # 식당 ID, 작성자 ID, 평점
    review_frame = pd.DataFrame(data=reviews, columns=("store_id", "user_id", "score"))


    return {"reviews": review_frame, "stores": store_frame}


def dump_dataframes(dataframes):
    pd.to_pickle(dataframes, DUMP_FILE)

def load_dataframes():
    return pd.read_pickle(DUMP_FILE)

data = import_data()
dump_dataframes(data)
data = load_dataframes()
dining_data = import_diningdata()

# 모든 가게 정보
global all_stores_data
all_stores_data = data["stores"]
print("--모든 가게 정보--")
print(all_stores_data.head())

# 평점 데이터 
ratings = data["reviews"]
print("--main-- 평점 데이터")
print(ratings.head())
ratings_source = [(ratings['user_id'][i], ratings['store_id'][i]) for i in range(ratings.shape[0])]
print("평점은 몇개임? ",ratings.shape[0])

# 음식점 데이터 
item_meta =dining_data["stores"]
print("--main-- 음식점 데이터")
print(item_meta.head())
print("item_meta 몇개임?? ", item_meta.shape[0])

item_meta = item_meta.reset_index()
item_feature_source = [(item_meta['store_id'][i], [ item_meta['category'][i], item_meta['average_rating'][i]] ) for i in range(item_meta.shape[0]) ]

dataset = Dataset()
dataset.fit(users=ratings['user_id'].unique(),
           items=ratings['store_id'].unique(),
           item_features=item_meta[item_meta.columns[1:]].values.flatten())

interactions, weights = dataset.build_interactions(ratings_source)
item_features = dataset.build_item_features(item_feature_source)


# Split Train, Test data
train, test = random_train_test_split(interactions, test_percentage=0.1)
train, test = train.tocsr().tocoo(), test.tocsr().tocoo()
train_weights = train.multiply(weights).tocoo()


# Define Search Space
trials = Trials()
space = [hp.choice('no_components', range(10, 50, 10)), hp.uniform('learning_rate', 0.01, 0.05)]



# Define Objective Function
global model
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


# Find Similar Items
def make_best_items_report(item_embeddings, store_id, num_search_items=10):
    item_id = store_id-1

    # Cosine similarity
    scores = item_embeddings.dot(item_embeddings[item_id])  # (10000, )
    item_norms = np.linalg.norm(item_embeddings, axis=1)    # (10000, )
    item_norms[item_norms == 0] = 1e-10
    scores /= item_norms

    # best: score가 제일 높은 item의 id를 num_search_items 개 만큼 가져온다.
    best = np.argpartition(scores, -num_search_items)[-num_search_items:]
    similar_item_id_and_scores = sorted(zip(best, scores[best] / item_norms[item_id]),
                                        key=lambda x: -x[1])

    # Report를 작성할 pandas dataframe
    best_items = pd.DataFrame(columns=['store_id','category','score'])
    global all_stores_data
    for similar_item_id, score in similar_item_id_and_scores:
        store_id = similar_item_id + 1
        
        print(store_id)
        print(all_stores_data[all_stores_data['store_id']==store_id].values)
        category = all_stores_data[all_stores_data['store_id']==store_id].values[0][2]
        
        # row = pd.Series([store_id, store_name, category,score], index=best_items.columns)
        row = pd.Series([store_id, category ,score], index=best_items.columns)
        best_items = best_items.append(row, ignore_index=True)

    return best_items

best_params = fmin(fn=objective, space=space, algo=tpe.suggest, max_evals=10, trials=trials)
item_biases, item_embeddings = model.get_item_representations(features=item_features)
report01 = make_best_items_report(item_embeddings, 2, 10)
report02 = make_best_items_report(item_embeddings, 1, 10)
print("2번 가게(카페) 와 유사한 음식점! ")
print(report01)
print("============")
print("1번가게(아구찜) 과 유사한 음식점! ")
print(report02)
