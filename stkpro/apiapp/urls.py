
from .views import get_stock_list,get_stock_by_symbol
from django.urls import path

urlpatterns = [
    path('get_stock_list',get_stock_list,name="get_stock_list"),
    path('get_stock_by_symbol',get_stock_by_symbol,name="get_stock_by_symbol"),
    
]
