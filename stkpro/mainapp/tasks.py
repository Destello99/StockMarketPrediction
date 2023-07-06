# Create your tasks here
from __future__ import absolute_import, unicode_literals
from os import name
# from celery import task
from mainapp.models import Stocks
from nsetools import Nse
from celery import shared_task
from stkPro.celery import app
from .models import Stocks, WatchList

from django.core.serializers import serialize

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

channel_layer = get_channel_layer()

@shared_task
def nse_stock_data():
    print('trying nse stock update')
    try:
        stock = Stocks.objects.all()
        nse = Nse()
        for sym in stock:
            try:
                res = nse.get_quote(sym.symbol)
                sym.name = res['companyName']
                sym.lastPrice = res['lastPrice']
                sym.change = res['pChange']
                sym.dayHigh = res['dayHigh']
                sym.dayLow = res['dayLow']
                sym.previousClose = res['previousClose']
                sym.save()
            except Exception as e:
                return e
                
        stk_obj = Stocks.objects.all()
        text_data = serialize("json", stk_obj)
        async_to_sync(channel_layer.group_send)('test_stock', {'type': 'send_stock_data', 'text': text_data})
        return True
    except Exception as e:
        raise Exception(e)


# @app.task(name='watch_list_data')  
# def watch_list_data(request):
#     user = request.user
#     watch_list_stocks_id = []
#     watch = WatchList.objects.filter(user = user)
#     for i in watch:
#         watch_list_stocks_id.append(i.stock.id)
#     stock = Stocks.objects.filter(id__in =watch_list_stocks_id)

#     nse = Nse()
#     stocks_detail = []
#     for sym in stock:
#         try:
#             res = nse.get_quote(sym.symbol)
#             sym.name = res['companyName']
#             sym.lastPrice = res['lastPrice']
#             sym.change = res['pChange']
#             sym.dayHigh = res['dayHigh']
#             sym.dayLow = res['dayLow']
#             sym.previousClose = res['previousClose']
#             sym.save()

#             stocks_detail.append(res['lastPrice'])
#         except Exception as e:
#             return e 
#     return stocks_detail




