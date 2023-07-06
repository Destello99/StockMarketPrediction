from django.contrib import admin
from django.contrib.auth.models import User
from .models import Stocks, UserProfile, WatchList
# Register your models here.



admin.site.register(Stocks)
admin.site.register(UserProfile)
admin.site.register(WatchList)