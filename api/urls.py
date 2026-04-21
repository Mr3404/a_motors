from django.urls import path
from .auction.views import *


urlpatterns = [
    path("make_list/", MakeView.as_view()),
    path("model_list/", ModelView.as_view()),
    path("upcoming_car_list/", UpcomingCarListView.as_view()),
    path("auction_car_list/", AuctionCarListView.as_view()),
]
