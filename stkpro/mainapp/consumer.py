# chat/consumers.py
import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from mainapp.models import Stocks
from mainapp.tasks import nse_stock_data
from django.core.serializers import serialize
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer

class getStocksConsumer(WebsocketConsumer):
    def connect(self):
        async_to_sync(self.channel_layer.group_add)(
            'test_stock',
            self.channel_name
        )

        stk = Stocks.objects.all()
        text_data = serialize("json", stk)

        self.accept()

        self.send(text_data)
        print("connected")
        

    def disconnect(self, close_code):
        self.channel_layer.group_discard('test_stock', self.channel_name)
        print("disconnected")


    def receive(self, text_data=None, bytes_data = None):
        text_dataa = json.loads(text_data)
        # print(text_dataa)
        channel_layer = get_channel_layer()
        channel_layer.send("demo",{
            "type": "application/json",
            "data" : text_dataa,
        })

        self.send(text_data = json.dumps({
            'payload': text_dataa
        }))

    def send_stock_data(self, event):
        '''
        Call back function to send message to the browser
        '''
        text_data = event['text']
        self.send(text_data)




# class getWatchListStockConsumer(WebsocketConsumer):
#     def connect(self):

#         self.room_name = 'test_watch_stock'
#         self.room_group_name = 'test_watch_stock'         #call this group name where we want data
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name,
#             self.channel_name
#         )
       
        
#         stk = Stocks.objects.all()
#         text_dataa = serialize("json", stk)
#         print(text_dataa)
#         self.accept()
#         self.send(text_data = text_dataa )
#         print("connected")
        

#     def disconnect(self, close_code):
#         print("disconnected")

#     def receive(self, text_data=None, bytes_data = None):
#         text_dataa = json.loads(text_data)
#         # print(text_dataa)
#         channel_layer = get_channel_layer()
#         channel_layer.send("demo",{
#             "type": "application/json",
#             "data" : text_dataa,
#         })


#         self.send(text_data = json.dumps({
#             'payload': text_dataa
#         }))



#     def send_watchlist_stock_data(self, event):
#         print("send notification")
#         print(event)
#         print("send notification")
#         # data = json.loads(event.get('value'))
#         # self.send(text_data = json.dumps({'payload':data}))
#         self.send(text_data = event.get('value'))