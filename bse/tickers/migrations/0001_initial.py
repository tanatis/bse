# Generated by Django 4.2.7 on 2023-11-28 14:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ticker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=5)),
                ('company_name', models.CharField(blank=True, max_length=30, null=True)),
                ('current_price', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.01)])),
            ],
        ),
    ]