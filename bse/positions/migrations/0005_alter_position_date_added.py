# Generated by Django 4.2.7 on 2023-12-05 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('positions', '0004_alter_positionhistory_date_added'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='date_added',
            field=models.DateField(),
        ),
    ]