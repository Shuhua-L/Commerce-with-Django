from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # (many-to-many)
    # watchlist :  User <->  Auction
    # bid : User <->  Auction
    # (one-to-many)
    # auction: User -> Auction
    # comment: User -> Comment

    class Meta:
        get_latest_by = "bid"
    

class Auction(models.Model):
    class Categories(models.TextChoices):
        NONSPECIFIC = 'NONSPECIFIC',
        FASHION = 'Fashion',
        TOYS = 'Toys',
        ELECTRONICS = 'Electronics',
        HOMEGOODS= 'Home Goods',
        WEAPONS = 'Weapons',
        ART = 'Art'

    # hidden fields
    seller = models.ForeignKey(User, on_delete=models.PROTECT, related_name="sales")
    is_active = models.BooleanField(default=True)

    #  required fields
    title = models.CharField(max_length=200)
    description = models.TextField()
    init_bid = models.PositiveIntegerField()

    # optional fields
    imageURL = models.URLField(blank=True)
    category = models.CharField(choices=Categories.choices, max_length=20, default=Categories.NONSPECIFIC)

    # relations
    fav = models.ManyToManyField(User, related_name="watchlist", blank=True)
    bids = models.ManyToManyField(User, related_name="bids", through='Bid', blank=True)

    def __str__(self):
        return self.title

class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    # extra fields
    price = models.PositiveIntegerField()
    edit_bid = models.BooleanField(default=True)

    def __str__(self):
        return f'Bid on {self.auction} (id:{self.id})'

    class Meta:
        ordering = ['auction','price']
        

class Comment(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

     # extra fields
    comment = models.TextField()
    date = models.DateField(default=datetime.now)
    edit_comment = models.BooleanField(default=True)

    def __str__(self):
        return f'Comment on {self.auction} (id:{self.id})'

    class Meta:
        ordering = ['auction','date']