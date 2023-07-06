import json
from django.dispatch import receiver
from django.db.models.signals import post_save

from django.core.serializers import serialize
from .models import Stocks
import channels.layers
from asgiref.sync import async_to_sync


@receiver(post_save, sender=Stocks)
def updated_stock_data(sender, instance, **kwargs):
    channel_layer = channels.layers.get_channel_layer()
    stk_obj = Stocks.objects.all()
    text_dataa = serialize("json", stk_obj)
    data = {
        'stock_detail' : text_dataa
    }
    async_to_sync(channel_layer.group_send)(
        'test_stock',  {
            'type' : 'send_stock_data',
            'value' : text_dataa
        }
    )
    instance.save()
    print("Called")
    
    
