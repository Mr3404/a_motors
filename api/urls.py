from django.urls import path
from .auction.views import *
from banner.views import BannerListView


urlpatterns = [
    path("make_list/", MakeView.as_view()),
    path("model_list/", ModelView.as_view()),
    path("upcoming_car_list/", UpcomingCarListView.as_view()),
    path("upcoming_car/<int:pk>/", UpcomingCarView.as_view()),
    path("auction_car_list/", AuctionCarListView.as_view()),
    path("auction_car/<int:pk>/", AuctionCarView.as_view()),
    
    path("banner_list/", BannerListView.as_view()),
]
