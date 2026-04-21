from rest_framework import serializers
from auction.models import *



class MakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Make
        fields = "__all__"
        
        
class ModelSerializer(serializers.ModelSerializer):
    make = MakeSerializer()
    class Meta:
        model = Model
        fields = "__all__"
        

class UpcomingCarListSerializer(serializers.ModelSerializer):
    model = ModelSerializer()
    auction_start_date = serializers.DateTimeField(format="%d.%m.%Y")
    class Meta:
        model = Car
        fields = ["id", "model", "year", "auction_start_date"]
        
        
class AuctionCarListSerializer(serializers.ModelSerializer):
    model = ModelSerializer()
    auction_end_date = serializers.DateTimeField(format="%d.%m.%Y")
    price = serializers.SerializerMethodField()
    class Meta:
        model = Car
        fields = ["id", "model", "year", "auction_end_date", "price"]
        
    def get_price(self, obj):
        if obj.current_price == 0 or obj.current_price is None:
            return obj.starting_price
        return obj.current_price
        