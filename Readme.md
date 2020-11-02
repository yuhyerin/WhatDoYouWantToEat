### 프로젝트 개요

##### \- 프로젝트 주제 : 음식점, 사용자 평점 기반 배달음식 추천 시스템

##### \- 프로젝트 기간 : 2020.08.31 ~ 2020.10.08

##### - 프로젝트 목적

-	사용자별 배달 음식점 평점을 분석하여 배달음식을 추천해주는 시스템
-	주소지 별 배달희망인원을 그룹화 하여 배달 최소금액 및 배달료 문제 완화 - 배달파티



##### - 추천시스템

lightfm 알고리즘을 활용한 협업필터링 + 컨텐츠기반필터링 (하이브리드)추천시스템을 적용하여, 사용자가 주문했던 음식점 내역을 기반으로 주문했던 음식점과 유사한 음식카테고리를 추천합니다.



##### \-배달파티


배달주최자(파티장)이 배달음식을 같이먹을 사람을 구하는 채팅방을 만든다


같이 주문에 참여할 인원(파티원)은 채팅방에 참여할 수 있다



##### \- 기술스택

![image](https://user-images.githubusercontent.com/44697835/95402712-58168480-094b-11eb-84c9-a26053ea8b36.png)



##### [ 실행방법 ]

##### \- frontend

```shell
npm i
npm run serve
```

##### \- backend

```shell
python manage.py runserver
```

##### - 설치해야 할 라이브러리

```shell
pip install mysqlclient
pip install pandas
pip install lightfm
pip install -U scikit-learn
pip install hyperopt
pip install Pillow
pip install pickle5
python -m pip install -U channels
python -m pip install channels_redis
```

##### \- 채팅구동을 위한 도커 실행

```shell
# 도커 설치 후 cmd에서 아래 명령어 실행
docker run -p 6379:6379 -d redis:5
```



