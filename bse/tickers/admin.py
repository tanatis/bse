from django.contrib import admin

from bse.tickers.models import Ticker


@admin.register(Ticker)
class TickerAdmin(admin.ModelAdmin):
    pass
