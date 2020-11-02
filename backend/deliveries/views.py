from django.shortcuts import render
from .models import Delivery
import json

# Create your views here.
def save_delivery(request):
    json_data = open('deliveries/delivery.json').read()
    json_d = json.loads(json_data)
    for i in range(len(json_d['data'])):
        delivery = Delivery()
        delivery.store_id = json_d['data'][i]['store_id']
        delivery.store_name = json_d['data'][i]['store_name']
        delivery.category = json_d['data'][i]['category']
        delivery.address = json_d['data'][i]['address']
        delivery.latitude = json_d['data'][i]['latitude']
        delivery.longitude = json_d['data'][i]['longitude']
        delivery.userid = json_d['data'][i]['user_id']
        delivery.score = json_d['data'][i]['score']
        delivery.reg_time = json_d['data'][i]['reg_time']
        delivery.day_type = json_d['data'][i]['day_type']
        delivery.save()
    return