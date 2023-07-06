from mainapp.models import Stocks
from rest_framework import serializers

class StocksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stocks
        fields = '__all__'




        