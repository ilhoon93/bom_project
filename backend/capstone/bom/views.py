from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from rest_framework import generics
from . import models
from . import serializers

import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient("mongodb://pungdeong:pungdeong@13.125.143.101/pungdeongBOM")
db=client.pungdeongBOM
modeltest=db.modeltest

def mongo_test(request):
    for log in db.raw_review_tier1.find():
        return HttpResponse(str(log))

def get_object(request):
    # product_DB에서 pname만 뽑아오기 
    for i in db.product_DB.find({"product.pid":'bom5832'},{'product.pname':1}):
        return HttpResponse(str(i))

# EB view
class IndexView(View):
    def get(self, request):
        return HttpResponse('<h1>EB Django Project</h1>')


class ListTodo(generics.ListCreateAPIView):
    queryset=models.Todo.objects.all()
    serializer_class=serializers.TodoSerializer
class DetailTodo(generics.RetrieveUpdateDestroyAPIView):
    queryset=models.Todo.objects.all()
    serializer_class=serializers.TodoSerializer


# 그래프 데이터 리스트 뷰
class poswc_list(generics.ListCreateAPIView):
    queryset=models.poswc.objects.all()
    serializer_class=serializers.poswc_serializer
class negwc_list(generics.ListCreateAPIView):
    queryset=models.negwc.objects.all()
    serializer_class=serializers.negwc_serializer
class dashboard_list(generics.ListCreateAPIView):
    queryset=models.dashboard.objects.all()
    serializer_class=serializers.dashboard_serializer

class bar_attribute_list(generics.ListCreateAPIView):
    queryset=models.bar_attribute.objects.all()
    serializer_class=serializers.bar_attribute_serializer
class bar_skin_list(generics.ListCreateAPIView):
    queryset=models.bar_skin.objects.all()
    serializer_class=serializers.bar_skin_serializer
class bar_channel_list(generics.ListCreateAPIView):
    queryset=models.bar_channel.objects.all()
    serializer_class=serializers.bar_channel_serializer
class pie_age_list(generics.ListCreateAPIView):
    queryset=models.pie_age.objects.all()
    serializer_class=serializers.pie_age_serializer
class hist_price_list(generics.ListCreateAPIView):
    queryset=models.hist_price.objects.all()
    serializer_class=serializers.hist_price_serializer
class map_positioning_list(generics.ListCreateAPIView):
    queryset=models.map_positioning.objects.all()
    serializer_class=serializers.map_positioning_serializer

# 저장 테스트
# from .models import product_DB
# class mongoview(**kwargs):
#     def get_mongo(self,queryset=None):
#         index=[i for i in product_DB.objects.mongo_aggergate([
#             {
#                 '$match':{
#                     'brandname':self.**kwargs['path'],
#                 }
#             },
#         ])] 
#         return index
    

# Create your views here.



    

