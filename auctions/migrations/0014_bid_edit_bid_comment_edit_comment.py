# Generated by Django 4.0.6 on 2022-08-23 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_comment_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='edit_bid',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='edit_comment',
            field=models.BooleanField(default=True),
        ),
    ]