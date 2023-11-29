from django.shortcuts import render
from django.views.generic import ListView
import requests
from bs4 import BeautifulSoup
from django.shortcuts import redirect

from bse.tickers.models import Ticker

BASE_URL = 'https://www.infostock.bg/infostock/control/quotes/'


def check_price(request, symbol):
    url = BASE_URL + symbol
    response = requests.get(url)
    website_html = response.text

    soup = BeautifulSoup(website_html, "html.parser")
    price = soup.find("span", id='price').text

    ticker = Ticker.objects.filter(symbol=symbol).get()
    ticker.current_price = float(price)
    ticker.save()

    return redirect('tickers_list')


class TickersListView(ListView):
    template_name = 'tickers/tickers_list.html'
    model = Ticker

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     return context
