from django.urls import path
from . import views


urlpatterns=[
    path('',views.ListTodo.as_view()),
    
    path('bar_skin',views.bar_skin_list().as_view(),name="bar_skin"),
    path('bar_attribute',views.bar_attribute_list().as_view(),name="bar_attribute"),
    path('bar_channel',views.bar_channel_list().as_view(),name="bar_channel"),
    path('pie_age',views.pie_age_list().as_view(),name="pie_age"),
    path('hist_price',views.hist_price_list().as_view(),name="hist_price"),
    path('map_positioning',views.map_positioning_list().as_view(),name="map_positioning"),
    path('poswc',views.poswc_list().as_view(),name="poswc"),
    path('negwc',views.negwc_list().as_view(),name="negwc"),
    path('dashboard',views.dashboard_list().as_view(),name="dashboard"),



    path('<int:pk>',views.DetailTodo.as_view()),
    path('mongo_test',views.mongo_test,name='mongo_test'),
    path('get_object',views.get_object,name='get_object'),
    # path('mongo_view',views.mongoview,name='mongoview'),
]