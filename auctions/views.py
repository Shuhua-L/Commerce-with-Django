
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.urls import reverse

from django.utils.translation import gettext_lazy as _

from .models import *
from .forms import *

# helper function
# that takes a list of auction listings
# and returns a nested list of (auction, price)
def with_prices(auctions):
    auctions_with_price = []
    for auc in auctions:
        bid = Bid.objects.filter(auction=auc).last().price
        auctions_with_price.append(list((auc, bid)))
    return auctions_with_price


def index(request):
    # a list of active auction listings
    active_auctions = Auction.objects.filter(is_active=True)

    return render(request, "auctions/index.html", {
        "auction_with_price": with_prices(active_auctions)
    })

def home(request):
    # a list of all auction listings, actice firsts
    all_auctions = Auction.objects.order_by('-is_active')

    return render(request, "auctions/index.html", {
        "auction_with_price": with_prices(all_auctions)
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    # Form submission, register a new user
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    # register view
    else:
        return render(request, "auctions/register.html")

def watchlist_view(request):
    user = request.user
    watchlist = user.watchlist.all()

    # Form submission, edit watchlist
    if request.method == "POST":
        id = request.POST["listingID"]
        listing = get_object_or_404(Auction, pk=id)
        if listing in watchlist:
            user.watchlist.remove(listing)
        else:
            user.watchlist.add(listing)
        
        # calling from index page
        if request.POST["origin"] == "index":
            return HttpResponseRedirect(reverse("watchlist"))
        # calling from listing page
        else:
            return HttpResponseRedirect(reverse("specific_listing", args={id}))

    # watchlist view
    else:
        return render(request, "auctions/index.html", {
            "message": f'{user}\'s watchlist:',
            "auction_with_price": with_prices(watchlist)
        })

def create(request):
    create_form = ListingForm()

    # Form submission, create a new auction listing
    if request.method == "POST":
        form = ListingForm(request.POST)

        if form.is_valid(): 
            listing = form.save(commit=False)
            listing.seller = request.user
            listing.save()

            listing.bids.add(request.user, through_defaults={'price': listing.init_bid})
            return HttpResponseRedirect(reverse("index"))
        else:
            create_form = form

    # create view
    else:
        return render(request, "auctions/create.html", {"form": create_form})

def category_view(request, cate=None):
    # category_view
    if not cate:
        categories_list = Auction.objects.values_list('category', flat=True).distinct()
        count_list = []
        for c in categories_list:
            count_list.append(list((c, Auction.objects.filter(category=c, is_active=True).count())))

        return render(request, "auctions/categories.html", {
            "cate_with_counts": count_list
        })
        
    # specific_category_view    
    else:
        listings = Auction.objects.filter(category=cate, is_active=True)
        return render(request, "auctions/index.html", {
            "auction_with_price": with_prices(listings),
            "message": f'Category: {cate}'
        })


def listing_view(request, id):
    # variables
    listing = get_object_or_404(Auction, pk=id)
    current_price = Bid.objects.filter(auction=listing).last().price
    comments = Comment.objects.filter(auction=listing)
    bid_form = BidForm()
    comment_form = CommentForm()
    message = None

    # Form submissions
    if request.method == "POST":
        # make a bit
        if 'edit_bid' in request.POST:
            form = BidForm(request.POST)
            if form.is_valid():
                bid = form.save(commit=False)

                # check if bid is appropriate
                if bid.price < current_price:
                    bid_form = form
                    message = "Bid should be greater than the current price. Try again."
                else:
                    bid.auction = listing
                    bid.user = request.user
                    bid.save()
                    return HttpResponseRedirect(reverse("specific_listing", args={id}))
            else:
                bid_form = form

        # add a comment
        if 'edit_comment' in request.POST:
            form = CommentForm(request.POST)
            if form.is_valid():
                cmt = form.save(commit=False)
                cmt.auction = listing
                cmt.user = request.user
                cmt.save()

                return HttpResponseRedirect(reverse("specific_listing", args={id}))

            else:
                comment_form = form

        # close auction 
        if 'close_auction' in request.POST:
            listing.is_active = False
            listing.save()
            return HttpResponseRedirect(reverse("specific_listing", args={id}))


    return render(request, "auctions/listing.html", {
        "listing": listing,
        "current_price": current_price,
        "comments": comments,
        "bid_form": bid_form,
        "comment_form": comment_form,
        "message": message
        })
    
