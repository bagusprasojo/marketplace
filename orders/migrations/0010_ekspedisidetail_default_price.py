# Generated by Django 4.2.20 on 2025-05-06 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_ekspedisi_ekspedisidetail'),
    ]

    operations = [
        migrations.AddField(
            model_name='ekspedisidetail',
            name='default_price',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
