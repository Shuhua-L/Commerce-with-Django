# Generated by Django 4.0.6 on 2022-08-30 17:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0015_alter_bid_options_alter_user_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['auction', 'date']},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'get_latest_by': 'bid'},
        ),
    ]
