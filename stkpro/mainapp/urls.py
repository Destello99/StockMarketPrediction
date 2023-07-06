from django.urls import path
from .views import index,base, stock_detail, search_stock,login,logout,register, user_profile, watch_list,save_watch_list, change_password, update_profile,predict,pre,chart



urlpatterns = [
    path('',index,name='index'),
    path('base',base,name='base'),
    path('stock/<str:stock_symbol>/',stock_detail,name='stock_detail'),
    path('search_stock',search_stock,name='search_stock'),
    path('login',login,name='login'),
    path('logout',logout,name='logout'),
    path('register',register,name='register'),
    path('user_profile/<str:user_name>/',user_profile,name='user_profile'),
    path('watch_list/<int:myid>/',watch_list,name='watch_list'),
    path('save_watch_list/<int:user_id>/<str:stock_symbol>/',save_watch_list,name='save_watch_list'),

    path('change_password',change_password,name='change_password'),
    path('update_profile/<int:myid>/',update_profile,name="update_profile"),
    path('predict',predict,name='predict'),
    path('pre',pre,name='pre'),
    path('chart',chart,name='chart'),




]


