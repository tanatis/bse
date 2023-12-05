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
    date_added = models.DateField(null=False, blank=False)

    def position_total(self):
        return self.count * self.price


class PositionHistory(models.Model):
    to_position = models.ForeignKey(Position, on_delete=models.CASCADE)
    date_added = models.DateField(blank=True, null=True)
    count = models.IntegerField(null=False, blank=False)
    price_per_share = models.FloatField(null=False, blank=False)
