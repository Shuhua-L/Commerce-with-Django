# Generated by Django 4.0.6 on 2022-08-17 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_alter_auction_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='category',
            field=models.CharField(choices=[('NONSPECIFIC', 'Nonspecific'), ('Fashion', 'Fashion'), ('Toys', 'Toys'), ('Electronics', 'Electronics'), ('Home Goods', 'Homegoods'), ('Weapons', 'Weapons'), ('Art', 'Art')], default='NONSPECIFIC', max_length=20),
        ),
    ]
