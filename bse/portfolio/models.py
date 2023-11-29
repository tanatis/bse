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
