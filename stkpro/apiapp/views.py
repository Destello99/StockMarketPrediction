from django.shortcuts import render
from rest_framework.response import Response
# Create your views here.
from .serializers import StocksSerializer
from mainapp.models import Stocks
from rest_framework.decorators import api_view
from django.http import Http404
from nsepy import get_history
from datetime import date, timedelta
import json

@api_view()
def get_stock_list(request):
    try:
        stok = Stocks.objects.all()
        stock_serializer = StocksSerializer(stok,many=True)
        return Response({'status':200,'payload':stock_serializer.data})
    except Exception as e:
        raise Http404("Stock not found")
    

@api_view()
def get_stock_by_symbol(request):
    try:

        now = date.today()
        # go back 3 months
        first = now.replace(day=1)
        lastMonth = first - timedelta(days=1)
        first = lastMonth.replace(day=1)
        lastMonth = first - timedelta(days=1)
        first = lastMonth.replace(day=1)
        lastMonth = first - timedelta(days=1)

        # get history
        data = get_history(symbol=request.GET['symbol'], start=date(lastMonth.year,lastMonth.month,lastMonth.day), end=date(now.year,now.month,now.day))
        # transpose to get better view of data
        data = data.transpose()
        # fix date to string for charts.
        data = {str(k): data[k].to_dict() for k in data}

        return Response({'status':200,'payload':data})
    except Exception as e:
        raise Http404("Stock not found")