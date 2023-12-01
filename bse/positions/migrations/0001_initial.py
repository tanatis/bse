# Generated by Django 4.2.7 on 2023-11-30 16:09

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tickers', '0001_initial'),
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(validators=[django.core.validators.MinValueValidator(1, message='Must be greater than 0')])),
                ('price', models.FloatField()),
                ('avg_price', models.FloatField()),
                ('date_added', models.DateField(auto_now_add=True)),
                ('ticker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tickers.ticker')),
                ('to_portfolio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portfolio.portfolio')),
            ],
        ),
    ]