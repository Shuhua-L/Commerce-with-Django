# Generated by Django 4.0.6 on 2022-08-12 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_alter_auction_category_alter_auction_init_bid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='category',
            field=models.CharField(choices=[('NONSPECIFIC', 'Nonspecific'), ('FASHION', 'Fashion'), ('TOYS', 'Toys'), ('ELECTRONICS', 'Electronics'), ('HOME', 'Home')], default=('NONSPECIFIC', 'Nonspecific'), max_length=20),
        ),
    ]
