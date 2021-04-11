# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
# from django.db import models
from django.db import models
class Todo(models.Model):
    objects=models.Manager()
    title = models.CharField(max_length=200)
    description = models.TextField()

# 피부타입 레이더차트 
class bar_skin(models.Model):
    objects=models.Manager()
    skin_type=models.CharField(max_length=100)
    count=models.IntegerField()
    def __str__(self):
        return self.skin_type
# 나이 파이차트
class pie_age(models.Model):
    objects=models.Manager()
    age_category=models.CharField(max_length=100)
    count=models.IntegerField()
    def __str__(self):
        return self.age_category
# 유통 막대그래프
class bar_channel(models.Model):
    objects=models.Manager()
    channel=models.CharField(max_length=100)
    count=models.IntegerField()
    def __str__(self):
        return self.channel
# 속성 막대 그래프
class bar_attribute(models.Model):
    objects=models.Manager()
    attribute=models.CharField(max_length=100)
    percent=models.IntegerField()
    def __str__(self):
        return self.attribute
# 가격 히스토그램
class hist_price(models.Model):
    objects=models.Manager()
    price=models.IntegerField()
    def __int__(self):
        return self.price
# 포지셔닝 맵
class map_positioning(models.Model):
    objects=models.Manager()
    pname=models.CharField(max_length=100)
    x_value=models.FloatField()
    y_value=models.FloatField()
    def __str__(self):
        return self.pname

# 긍정 워드클라우드
class poswc(models.Model):
    objects=models.Manager()
    words=models.CharField(max_length=100)
    count=models.IntegerField()
    setval=models.IntegerField()
    def __str__(self):
        return self.words

#부정 워드클라우드
class negwc(models.Model):
    objects=models.Manager()
    words=models.CharField(max_length=100)
    count=models.IntegerField()
    setval=models.IntegerField()
    def __str__(self):
        return self.words

# 감성 대시보드 

class dashboard(models.Model):
    objects=models.Manager()
    sentdate=models.CharField(max_length=100)
    sentscore=models.IntegerField()
    def __str__(self):
        return self.sentdate


