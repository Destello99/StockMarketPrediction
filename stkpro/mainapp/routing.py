from django.urls import path, include
from .import consumer

websocket_urlpatterns = [
    path('ws/get_stocks/', consumer.getStocksConsumer.as_asgi()),
    # path('ws/get_watchlist_stocks/', consumer.getWatchListStockConsumer.as_asgi()),

]