from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.forms import Textarea
from django.forms import ModelForm
from django.forms import ModelChoiceField
from django.forms import ChoiceField
from django.db import models
from .models import Category, Listing, User, Bid, Watch, Comment

from .models import User

WATCHLIST=[('yes', 'Yes'), ('no', 'No')]
watchlist = False
active_toggle = True
category_toggle = False
category_filter = Category.objects.all()

class AddComment(forms.Form):
    comment = forms.CharField(max_length=256, widget=forms.Textarea
        (attrs={'placeholder':'Add comment', 'rows':5, 'style':'height: auto;'}), label='')

# class Newlisting(forms.Form):
#     title = forms.CharField(max_length=256, widget=forms.TextInput(attrs={'placeholder':'Add title', 'style':'width: 300px;'}), label='')
#     description = forms.CharField(max_length=1024, widget=forms.Textarea(attrs={'placeholder':'Add description', 'rows':10, 'style':'height: auto; width: 300px;'}), label='')
#     starting_bid = forms.DecimalField(max_digits=12, decimal_places=2, widget=forms.NumberInput(attrs={'placeholder':'Add starting bid', 'style':'width: 300px;'}), label='')
#     image_url = forms.URLField(max_length=200, widget=forms.URLInput(attrs={'placeholder':'Add image URL (optional)', 'style':'width: 300px;'}), label='', required=False)
#     category = forms.ModelChoiceField(queryset=Category.objects.all().order_by('category'), empty_label="Select category", label='', widget=forms.TextInput(attrs={'placeholder':'Select category','style':'width: 300px;'}))

class Newlisting(ModelForm):
    # image_url = models.CharField(null=True, blank=True)

    class Meta:
        model = Listing
        fields = ['title', 'description', 'starting_bid', 'image_url', 'category']
        labels = {
            "title": '',
            "description": '',
            "starting_bid": '',
            "image_url": ''
            # "category": ''
        }

        widgets = {
            "title": forms.TextInput(attrs={'placeholder': 'Enter title', "style": "width: 350px"}),
            "description": forms.Textarea(attrs={'placeholder': 'Enter description', "style": "width: 350px"}),
            "starting_bid": forms.NumberInput(attrs={'placeholder': 'Enter starting bid', "style": "width: 350px"}),
            "image_url": forms.URLInput(attrs={'placeholder': 'Enter image URL (optional)', "style": "width: 350px"}),
            "category": forms.Select(attrs={'empty_label':"Select category", "style": "width: 278px"})

        }

class Newbid(forms.Form):
    bid_amount = forms.DecimalField(max_digits=12, decimal_places=2, label='', widget=forms.NumberInput
        (attrs={'placeholder':'Add bid', 'style':'width: 300px;'}))




def index(request, category_id = 0):
    
    global active_toggle
    global category_toggle
    global watchlist
    global category_filter

    if category_id == 0:
        category = "All"
        category_toggle = False
    else:
        category_filter = Category.objects.get(id=category_id)
        category = category_filter.category
        category_toggle = True

    if request.method == "POST":
        if 'watchlist_on' in request.POST:
            watchlist = True
            return HttpResponseRedirect(reverse("index", kwargs={"category_id": category_id}))   
        elif 'watchlist_off' in request.POST:
            watchlist = False
            return HttpResponseRedirect(reverse("index", kwargs={"category_id": category_id})) 
        elif 'closed_on' in request.POST:
            active_toggle = False
            return HttpResponseRedirect(reverse("index", kwargs={"category_id": category_id})) 
        elif 'closed_off' in request.POST:
            active_toggle = True
            return HttpResponseRedirect(reverse("index", kwargs={"category_id": category_id})) 

    listings = Listing.objects.filter(active=active_toggle)
    if watchlist == True:
        listings = listings.filter(watch__user=request.user)
    if category_toggle == True:
        listings = listings.filter(category=category_filter)

    return render(request, "auctions/index.html", {"listings": listings, "categories": Category.objects.all(),
        "watchlist": watchlist, "active_toggle": active_toggle, "category_toggle":category_toggle, "category": category})

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
    else:
        return render(request, "auctions/register.html")

@login_required
def listingcreate(request):


    if request.method == 'POST':
        newlisting = Newlisting(request.POST)
        if newlisting.is_valid():
            nl = newlisting.save(commit=False)
            nl.active = True
            nl.user = request.user
            nl.save()
            return HttpResponseRedirect(reverse('listingview', kwargs={"listing_id": nl.id}))
            


        # if newlisting.is_valid():
        #     new_listing = Listing() 
        #     new_listing.title = newlisting.cleaned_data["title"]
        #     new_listing.description = newlisting.cleaned_data["description"]
        #     new_listing.starting_bid = newlisting.cleaned_data["starting_bid"]
        #     new_listing.image_url = newlisting.cleaned_data["image_url"]
        #     new_listing.category = newlisting.cleaned_data["category"]
        #     new_listing.user = request.user
        #     new_listing.active = True
        #     new_listing.save()

        # return HttpResponseRedirect(reverse("listingcreate"))

    newlisting = Newlisting()
    return render(request, "auctions/listingcreate.html", {"newlisting": newlisting})


def listingview(request, listing_id):
    listing_current = Listing.objects.get(id=listing_id)
    winning_bidder = None
    message = ""
    bids = Bid.objects.filter(listing = listing_current)
    seller_login = False
    watching = False
    max_bid = 0


    if request.user.is_authenticated:
        if request.method == 'POST' and 'watchlist' in request.POST:
            if len(Watch.objects.filter(user=request.user, listing=listing_current)) == 0:
                watch = Watch()
                watch.user = request.user
                watch.listing = listing_current
                watch.save()
            else:
                Watch.objects.filter(user=request.user, listing=listing_current).delete()
    
        if request.method == 'POST' and 'comment' in request.POST:
            addComment = AddComment(request.POST)
            if addComment.is_valid():
                if addComment.cleaned_data["comment"] != '':
                    newComment = Comment()
                    newComment.comment = addComment.cleaned_data["comment"]
                    newComment.user = request.user
                    newComment.listing = listing_current
                    newComment.save()
                return HttpResponseRedirect(reverse("listingview", kwargs={"listing_id": listing_id}))

    for bid in bids:
        if bid.bid_amount > max_bid:
            max_bid = bid.bid_amount
    if request.user.is_authenticated: 
        if listing_current.user == request.user:
            seller_login = True
            if request.method == 'POST' and 'end_listing' in request.POST:
                listing_current.active = False
                listing_current.save(update_fields=["active"])
        else:
            seller_login = False
            if request.method == 'POST' and 'new_bid' in request.POST:
                new_bid_amount = Newbid(request.POST)
                if new_bid_amount.is_valid():
                    new_bid_cleaned = new_bid_amount.cleaned_data['bid_amount']
                    if new_bid_cleaned > listing_current.starting_bid and new_bid_cleaned > max_bid:
                        new_bid = Bid()
                        new_bid.bid_amount = new_bid_amount.cleaned_data['bid_amount']
                        new_bid.user = request.user
                        new_bid.listing = listing_current
                        new_bid.save()
                    else:
                        message = "Bid must be greater than current highest bid"
    
    bids = Bid.objects.filter(listing = listing_current)
    count_bid = len(bids)
    max_bid = 0
    for bid in bids:
        if bid.bid_amount > max_bid:
            winning_bidder = bid.user
            max_bid = bid.bid_amount


    if request.user.is_authenticated: 
        if len(Watch.objects.filter(user=request.user, listing=listing_current)) == 0:
            watching = False
        else:
            watching = True

    new_bid_amount = Newbid()
    addComment = AddComment()
    comments = Comment.objects.filter(listing=listing_current)
    return render(request, "auctions/listingview.html", {"listing": listing_current, "listing_id": listing_id,
        "new_bid_amount": new_bid_amount, "max_bid": max_bid, "winning_bidder": winning_bidder, "count_bid": count_bid, 
        "active": listing_current.active, "seller_login": seller_login, "current_user": request.user, "message": message,
        "watching": watching, "addComment": addComment, "comments": comments})

def categories(request):
    return render(request, "auctions/categories.html", {"categories": Category.objects.all()})
