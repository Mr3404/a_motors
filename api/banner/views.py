from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from banner.models import Banner
from .serializers import BannerSerializer


class BannerListView(APIView):
    def get(self, request):
        try:
            banners = Banner.objects.all()
            serializer = BannerSerializer(banners, many=True)
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)