from django.core.validators import MinValueValidator
from django.db import models

from bse.portfolio.models import Portfolio
from bse.tickers.models import Ticker


class Position(models.Model):
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE)
    to_portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    count = models.IntegerField(blank=False, null=False, validators=[MinValueValidator(1, message='Must be greater than 0')])
    price = models.FloatField()
    avg_price = models.FloatField()
    date_added = models.DateField(auto_now_add=True)

    def position_total(self):
        return self.count * self.price
