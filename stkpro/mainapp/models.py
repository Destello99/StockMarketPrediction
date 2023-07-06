import json
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from channels.layers import get_channel_layer
from django.dispatch import receiver
from django.db.models.signals import post_save
from asgiref.sync import async_to_sync
from django.core.serializers import serialize
from nsetools import Nse
nse = Nse()

# Create your models here.


class Stocks(models.Model):
    name = models.CharField(max_length=100,blank=True,null=True)
    symbol = models.CharField(max_length=100,blank=True,null=True)          #, unique=True
    lastPrice = models.DecimalField(max_digits=6,decimal_places=2,blank=True,null=True)
    change = models.DecimalField(max_digits=6,decimal_places=2,blank=True,null=True)
    dayHigh = models.DecimalField(max_digits=6,decimal_places=2,blank=True,null=True)
    dayLow = models.DecimalField(max_digits=6,decimal_places=2,blank=True,null=True)
    previousClose = models.DecimalField(max_digits=6,decimal_places=2,blank=True,null=True)

    def __str__(self):
        return self.name


    def save(self, *args, **kwargs):
        sy = self.symbol
        is_avail = False
        try:
            out = nse.get_quote(sy)
            is_avail = True
        except:
            return False

        # print("save called")
        if is_avail:
            super(Stocks, self).save(*args, **kwargs)
        else:
            raise ValueError("Given Symbol is not valid")


# @receiver(post_save, sender=Stocks)
# def updated_stock_data(sender, instance, **kwargs):
#     instance.stocks.save()
    
    

    



class UserProfile(models.Model):
    user = models.OneToOneField(to=User,on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=15,blank=True,null=True)
    address = models.TextField(blank=True,null=True)
    photo = models.ImageField(upload_to="user_photo",blank=True,null=True)




class WatchList(models.Model):
    user = models.ForeignKey(to=User,on_delete=models.CASCADE)
    stock = models.ForeignKey(to=Stocks,on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return self.user.username + " => " + self.stock.symbol





