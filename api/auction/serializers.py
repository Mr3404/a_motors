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
        
        
class CarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = "__all__"

class UpcomingCarListSerializer(serializers.ModelSerializer):
    model = ModelSerializer()
    auction_start_date = serializers.DateTimeField(format="%d.%m.%Y")
    image = serializers.SerializerMethodField()
    class Meta:
        model = Car
        fields = ["id", "model", "year", "auction_start_date", "image"]
        
    def get_image(self, obj):
        image = obj.car_image.first()
        if image:
            return image.image.url
        return None
        
        
class AuctionCarListSerializer(serializers.ModelSerializer):
    model = ModelSerializer()
    auction_end_date = serializers.DateTimeField(format="%d.%m.%Y")
    price = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    class Meta:
        model = Car
        fields = ["id", "model", "year", "auction_end_date", "price", "image"]
        
    def get_price(self, obj):
        if obj.current_price == 0 or obj.current_price is None:
            return obj.starting_price
        return obj.current_price
        
    def get_image(self, obj):
        image = obj.car_image.first()
        if image:
            return image.image.url
        return None
    