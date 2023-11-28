from django.urls import path
from bse.tickers.views import TickersListView, check_price

urlpatterns = [
    path('tickers/', TickersListView.as_view(), name='tickers_list'),
    path('check/<str:symbol>/', check_price, name='check_price'),
]
