from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from auction.models import *
from .serializers import *


class MakeView(APIView):
    def get(self, request):
        try:
            make_list = Make.objects.all()
            serializer = MakeSerializer(make_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        
class ModelView(APIView):
    def get(self, request):
        try:
            model_list = Model.objects.all()
            serializer = ModelSerializer(model_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        
class UpcomingCarListView(APIView):
    def get(self, request):
        try:
            car_list = Car.objects.filter(status="upcoming")
            if request.query_params.get("make"):
                car_list = car_list.filter(model__make__name=request.query_params.get("make"))
            if request.query_params.get("model"):
                car_list = car_list.filter(model__name=request.query_params.get("model"))
            if request.query_params.get("year_range"):
                year_range = request.query_params.get("year_range").split("-")
                car_list = car_list.filter(year__gte=int(year_range[0]), year__lte=int(year_range[1]))
            serializer = UpcomingCarListSerializer(car_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        
class AuctionCarListView(APIView):
    def get(self, request):
        try:
            car_list = Car.objects.filter(status="active")
            if request.query_params.get("make"):
                car_list = car_list.filter(model__make__name=request.query_params.get("make"))
            if request.query_params.get("model"):
                car_list = car_list.filter(model__name=request.query_params.get("model"))
            if request.query_params.get("year_range"):
                year_range = request.query_params.get("year_range").split("-")
                car_list = car_list.filter(year__gte=int(year_range[0]), year__lte=int(year_range[1]))
            serializer = AuctionCarListSerializer(car_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)