from django.core.validators import MinValueValidator
from django.db import models


class Ticker(models.Model):
    symbol = models.CharField(max_length=5, blank=False, null=False)
    company_name = models.CharField(max_length=30, blank=True, null=True)
    current_price = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0.01)])

    def __str__(self):
        return f'{self.symbol} - {self.company_name}'
