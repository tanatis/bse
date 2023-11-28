# import requests
# from bs4 import BeautifulSoup
# from django.shortcuts import redirect
#
# from bse.tickers.models import Ticker
#
# BASE_URL = 'https://www.infostock.bg/infostock/control/quotes/'
#
#
# def check_price(pk):
#     ticker = Ticker.objects.filter(pk=pk).get()
#     url = BASE_URL + ticker.symbol.upper()
#
#     response = requests.get(url)
#     website_html = response.text
#
#     soup = BeautifulSoup(website_html, "html.parser")
#     price = soup.find("span", id='price').text
#
#     ticker.current_price = float(price)
#     ticker.save()
#
#     return redirect('tickers_list')
