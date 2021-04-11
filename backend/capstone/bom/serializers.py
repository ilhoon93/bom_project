from rest_framework import serializers
from . import models


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'title',
            'description',
        )
        model = models.Todo

class bar_skin_serializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'skin_type',
            'count',
        )
        model = models.bar_skin

class pie_age_serializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'age_category',
            'count',
        )
        model = models.pie_age

class bar_channel_serializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'channel',
            'count',
        )
        model = models.bar_channel

class bar_attribute_serializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'attribute',
            'percent',
        )
        model = models.bar_attribute

class hist_price_serializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'price',
        )
        model = models.hist_price

class map_positioning_serializer(serializers.ModelSerializer):
    class Meta:
        fields=(
            'id',
            'pname',
            'x_value',
            'y_value',
        )
        model = models.map_positioning

class poswc_serializer(serializers.ModelSerializer):
    class Meta:
        fields=(
            'id',
            'words',
            'count',
            'setval',
        )
        model = models.poswc

class negwc_serializer(serializers.ModelSerializer):
    class Meta:
        fields=(
            'id',
            'words',
            'count',
            'setval',
        )
        model = models.negwc

class dashboard_serializer(serializers.ModelSerializer):
    class Meta:
        fields=(
            'id',
            'sentdate',
            'sentscore',
        )
        model = models.dashboard