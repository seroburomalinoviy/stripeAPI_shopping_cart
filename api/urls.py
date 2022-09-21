from django.contrib import admin
from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path('^$', views.index, name='index'),
    re_path(r'^item/(?P<item_id>\d+)/$', views.item, name='item'),
    re_path(r'^buy/(?P<buy_id>\d+)/$', views.buy, name='buy'),
    re_path(r'^success$',views.success, name='success' ),
    re_path(r'^cancelled',views.cancelled, name='cancelled' ),
]