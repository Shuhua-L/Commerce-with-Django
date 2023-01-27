# Generated by Django 4.0.6 on 2022-08-30 17:15

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_bid_edit_bid_comment_edit_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bid',
            options={'ordering': ['auction', 'price']},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'get_latest_by': 'bids'},
        ),
        migrations.AlterField(
            model_name='auction',
            name='bids',
            field=models.ManyToManyField(blank=True, related_name='bids', through='auctions.Bid', to=settings.AUTH_USER_MODEL),
        ),
    ]