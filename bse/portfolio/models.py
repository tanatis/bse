from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

UserModel = get_user_model()


class Portfolio(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False, verbose_name='Portfolio name')
    cash = models.FloatField(blank=True, null=True, default=0, validators=[MinValueValidator(0, message='Cannot be negative number!')])
    create_date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class CashOperations(models.Model):
    OPERATIONS = (
        ('deposit', 'Deposit'),
        ('withdraw', 'Withdraw'),
    )
    operation = models.CharField(choices=OPERATIONS, max_length=8, blank=False, null=False)
    amount = models.FloatField(blank=False, null=False, validators=[MinValueValidator(0.01, message='Must be greater than 0!')])
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    date_added = models.DateField(auto_now_add=True)
