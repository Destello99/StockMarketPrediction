import json
import re
from django.shortcuts import render, redirect,HttpResponse, get_object_or_404
from django.shortcuts import render
from nsetools import Nse
from .models import Stocks, WatchList
import requests
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile
import pickle
from .import consumer

import pickle
from .finalModel import my_pickled_object

import matplotlib.pyplot as plt

from io import BytesIO
import base64
import channels.layers
from asgiref.sync import async_to_sync
from pandas import *
# Create your views here.





def nse_stock_data():
    stock = Stocks.objects.all()
    nse = Nse()
    stocks_detail = []
    for sym in stock:
        res = nse.get_quote(sym.symbol)
        stocks_detail.append(res)
    return stocks_detail
    

def index(request):
    x = nse_stock_data()
    # print(x)
    context = {
        'stocks': x
    }
    return render(request,'index.html',context)


def base(request):
    try:
        user = request.user
    except:
        pass
    x = nse_stock_data()
    # print(x)
    context = {
        'stocks': x
    }
    return render(request,'base.html',context)




def stock_detail(request,stock_symbol):
    symbol = stock_symbol
    nse = Nse()
    try:
        res = nse.get_quote(symbol)
        if not res:
            messages.info(request,"Symbol not registered in US Stocks")
            return render(request,'stock_detail.html')
        else:
            # print(res)
            # print("type : ",type(res))
            
            context = {
                'stock_detail' : res,
                'symbol' : symbol
            }
            return render(request,'stock_detail.html',context)
    except Exception as e:
        messages.info(request,"Symbol not registered in US Stocks")
        return render(request,'stock_detail.html')
    # return render(request,'stock_detail.html')




def search_stock(request):
    nse = Nse()
    try:
        symbol = request.GET['symbol']
        res = nse.get_quote(symbol)
        # print(res)
        # print("type : ",type(res))
        if not res:
            messages.info(request,"Symbol not registered in US Stocks")
            return render(request,'stock_detail.html')
        else:
            
            context = {
                'stock_detail' : res,
                'symbol' : symbol
            }
            return render(request,'stock_detail.html',context)
    except:
        messages.info(request,"Symbol not registered in US Stocks")
        return render(request,'stock_detail.html')




def login(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']

        user=auth.authenticate(username=username, password=password)
        if user is not None:
            try:
                auth.login(request,user)
                return redirect("/")
                
            except:
                messages.info(request,'You are not patient account')
                return render(request,'login.html')
        else:
            messages.info(request,'invalid credentials')
            return redirect("login")
    else:    
        return render(request,'login.html')




def logout(request):
    user = request.user
    auth.logout(request)
    return redirect('login')




def register(request):
    if request.method=='POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['pass']
        password2 = request.POST['cpass']


        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,"Username already taken")
                return redirect('register')

            elif User.objects.filter(email=email).exists():
                messages.info(request,"Email-id already taken")
                return redirect('register')
            else:
                
                user = User.objects.create_user(username=username,email=email,password = password1,first_name = fname,last_name=lname)
                user.save()
                auth.login(request,user)
                pat_pro = UserProfile.objects.create(user = user)
                pat_pro.save()
                return redirect('/')
                   
        else:
            messages.info(request," Both Password are not match")
            return redirect('register')
    else:
        return render(request, 'register.html')



def user_profile(request,user_name):
    user = request.user
    
    return render(request,'user_profile.html')






def watch_list(request,myid):
    usr = User.objects.get(pk = myid)
    print("USER : ",usr)
    wa = WatchList.objects.filter(user = usr)
    print("WA : ",wa)
    watch_list_stocks_id = []
    watch_list_stocks_symbol = []
    for i in wa:
        watch_list_stocks_id.append(i.stock.id)
        watch_list_stocks_symbol.append(i.stock.symbol)
    watch = Stocks.objects.filter(id__in =watch_list_stocks_id)
    print(watch_list_stocks_id)
    watch_list_stocks_symbol = set(watch_list_stocks_symbol)
    watch_list_stocks_symbol = list(watch_list_stocks_symbol)
    context = {
        'watch' : watch,
        'stock_symbol' : watch_list_stocks_symbol,

    }
    return render(request,'watch_list.html',context)




def save_watch_list(request,user_id,stock_symbol):
    stock_symbol = stock_symbol.upper()
    usr = User.objects.get(pk = user_id)
    try:
        stock = Stocks.objects.get(symbol = stock_symbol)
        try:
            wa = WatchList.objects.filter(user = usr,stock = stock)
            print("total sytocks we get available : ",len(wa))
            print("AVAILABLE : ",wa)
            if len(wa) > 0:
                print("Already Available in watchlist")
                messages.info(request,"Stock is already in your watch List")
                return redirect('watch_list', user_id)
            else:
                print(stock)
                watch = WatchList.objects.create(user = usr,stock = stock)
                watch.save()
                messages.info(request,"Stock addedd in your watchlist")
        except:
            pass
        
    except Exception as e:
        messages.info(request,"You cant add this stock")
        return redirect('watch_list', user_id)

    return redirect('watch_list', user_id)




def update_profile(request,myid):
    try:
        if request.method == "POST":
            usr = User.objects.get(pk=myid)
            user_profile = UserProfile.objects.get(user = usr)
            usr.first_name = request.POST['fname']
            usr.last_name = request.POST['lname']
            user_profile.mobile_number = request.POST['mobile']
            user_profile.address = request.POST['address']
            usr.save()
            user_profile.save()
            messages.info(request,"User Profiel Updated")
            return redirect('user_profile',usr.username)
    except Exception as e:
        messages.info(request,e)
        return redirect('user_profile',usr.username)




def change_password(request):
    return render(request,'change_password.html')

pkl = pickle.loads(my_pickled_object)  # Unpickling the object

def predict(request):
    
    return render(request,'predict.html')


def pre(request):
    if request.method == 'POST':
        n= int(request.POST['year'])
        store_sbin = pkl.arima_mod(pkl.sbin_df,n*365)
        store_tatamotors = pkl.arima_mod(pkl.tatamotors_df,n*365)
        store_bpcl = pkl.arima_mod(pkl.bpcl_df,n*365)
        store_adaniports = pkl.arima_mod(pkl.ADANIPORTS_df,n*365)
        store_hdfcbank = pkl.arima_mod(pkl.HDFCBANK_df,n*365)
        
        last_sbin = pkl.sbin_df['Price'].iloc[-1]
        last_tatamotors= pkl.tatamotors_df['Price'].iloc[-1] 
        last_bpcl=pkl.bpcl_df['Price'].iloc[-1] 
        last_hdfc=pkl.HDFCBANK_df['Price'].iloc[-1] 
        last_adaniports=pkl.ADANIPORTS_df['Price'].iloc[-1] 
    
    
    # Combining Forecasting Value of both Gold and General Bond 
        forecast_df=store_sbin["Forecasted_value"]
        forecast_df=forecast_df.to_frame()
        forecast_df["TATAMOTORS"]=store_tatamotors["Forecasted_value"]
        forecast_df["BPCL"]=store_bpcl["Forecasted_value"]
        forecast_df["ADANIPORTS"]=store_adaniports["Forecasted_value"]
        forecast_df["HDFCBANK"]=store_hdfcbank["Forecasted_value"]
     
    
        forecast_df.rename(columns = {'Forecasted_value':'SBIN'}, inplace = True)
        forecast_df=forecast_df.round(5)

        img = BytesIO()
        forecast_df1 =  forecast_df.cumsum()
        plt.figure()
        forecast_df1.plot()
        plt.savefig(img, format='png')
        plt.close()
        img.seek(0)

        plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    
    # saving the dataframe
        SBIN=pkl.sbin_df
        BPCL=pkl.bpcl_df
        TATAMOTORS=pkl.tatamotors_df
        ADANIPORTS=pkl.ADANIPORTS_df
        HDFCBANK=pkl.HDFCBANK_df
    
        SBIN.to_csv('SBIN.csv',header=True,index=True)
        BPCL.to_csv('BPCL.csv',header=True,index=True)
        TATAMOTORS.to_csv('TATAMOTORS.csv',header=True,index=True)
        ADANIPORTS.to_csv('ADANIPORTS.csv',header=True,index=True)
        HDFCBANK.to_csv('HDFCBANK.csv',header=True,index=True)
   
        forecast_df.to_csv('forecast.csv', header=True, index=True)
        return redirect('chart')
    return redirect('predict')



def chart(request):

    data = read_csv("forecast.csv")
    cols=[0]
    r = read_csv("forecast.csv", index_col=0, usecols=cols)
    
    date=r.index.tolist()
    sbin=data['SBIN'].tolist()
    tatamotors=data['TATAMOTORS'].tolist()
    bpcl=data['BPCL'].tolist()
    adaniports=data['ADANIPORTS'].tolist()
    hdfc=data['HDFCBANK'].tolist()

    sbin_buy=False
    tatamotors_buy=False
    bpcl_buy=False
    adaniports_buy=False
    hdfc_buy=False

    if sbin[1]<sbin[-1]:
        sbin_buy=True
    
    if tatamotors[1]<tatamotors[-1]:
        tatamotors_buy=True
    
    if bpcl[1]<bpcl[-1]:
        bpcl_buy=True
    
    if adaniports[1]<adaniports[-1]:
        adaniports_buy=True
    
    if hdfc[1]<hdfc[-1]:
        hdfc_buy=True

    print(sbin_buy,tatamotors_buy,bpcl_buy,adaniports_buy,hdfc_buy)
    
    print(type(sbin))
    context={"labels": json.dumps(date),"sbin": json.dumps(sbin), "tatamotors": json.dumps(tatamotors),"bpcl":json.dumps(bpcl),"adaniports":json.dumps(adaniports),"hdfc":json.dumps(hdfc),
            'sbin_buy':sbin_buy,'tatamotors_buy':tatamotors_buy,'bpcl_buy':bpcl_buy,'adaniports_buy':adaniports_buy,'hdfc_buy':hdfc_buy}
    
    return render(request, 'chart.html', context)

# def practice(request):
#     user = request.user
#     watch_list_stocks_id = []
#     watch = WatchList.objects.filter(user = user)
#     for i in watch:
#         watch_list_stocks_id.append(i.stock.id)
#     stock = Stocks.objects.filter(id__in =watch_list_stocks_id)
#     print(stock)
#     return HttpResponse(stock)