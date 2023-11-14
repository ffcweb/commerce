from pyexpat.errors import messages
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from .models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .models import Listing, Bid, Comment, Category,Watchlist
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ListingForm, BidForm  # need to create a BidForm to handle bid input
from django.db import transaction



# -----------------------------------------------------------
# def index(request):
#     return render(request, "auctions/index.html")


def index(request):
    active_listings = Listing.objects.filter(is_active=True)
    return render(request, 'auctions/index.html', {'active_listings': active_listings})


def create_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)  # Include request.FILES to handle image uploads
        if form.is_valid():
            # Save the form and associate it with the logged-in user
            listing = form.save(commit=False)
            listing.creator = request.user
            listing.save()
            return redirect('index')  # Redirect to the index page after creating the listing
    else:
        form = ListingForm()

    categories = Category.objects.all()
    return render(request, 'auctions/create_listing.html', {'categories': categories, 'form': form})


def category_list(request):
    categories = Category.objects.annotate(num_listings=Count('listings')).filter(num_listings__gt=0)
    return render(request, 'auctions/category_list.html', {'categories': categories})


def category_detail(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    active_listings = category.listings.filter(is_active=True)
    return render(request, 'auctions/category_detail.html', {'category': category, 'active_listings': active_listings})

# ==========================bid, close_listing, add_comment: =================================
# need to create the corresponding templates (close_listing.html for the close_listing view)
# need to update your URL patterns to include these new views.
# bid view: Allows users to place bids on active listings.
# Validates the bid amount and updates the current bid if the new bid is higher
# ==========================================================================

@login_required
def bid(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id, is_active=True)

    if request.method == 'POST':
        form = BidForm(request.POST)

        if form.is_valid():
            bid_amount = form.cleaned_data['bid_amount']

            if listing.current_bid is not None and bid_amount is not None:
                if bid_amount > listing.current_bid:
                    Bid.objects.create(listing=listing, bidder=request.user, bid_amount=bid_amount)
                    listing.current_bid = bid_amount
                    listing.save()

                    return redirect('listing_detail', listing_id=listing_id)
                else:
                    return HttpResponseForbidden("Your bid must be higher than the current bid.")
            else:
                return HttpResponseForbidden("Invalid bid amount or current bid.")

        else:
            # Render the form with errors
            return render(request, 'auctions/place_bid.html', {'form': form, 'listing': listing})
    else:
        form = BidForm()

    return render(request, 'auctions/place_bid.html', {'form': form, 'listing': listing})

# ======================== close_listing ======================================
# # close_listing view: Allows the creator of a listing to close it.
# # Only available for active listings.
# @login_required
# def close_listing(request, listing_id):
#     listing = get_object_or_404(Listing, pk=listing_id, creator=request.user, is_active=True)
#     if request.method == 'POST':
#         listing.is_active = False
#         listing.save()
#         return redirect('listing_detail', listing_id=listing_id)
#     return render(request, 'auctions/close_listing.html', {'listing': listing})
@login_required
def close_listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id, creator=request.user, is_active=True)

    if request.method == 'POST':
        with transaction.atomic():
            listing.is_active = False
            listing.save()
            return redirect('listing_detail', listing_id=listing_id)

    # Handle non-POST requests
    return render(request, 'auctions/close_listing.html', {'listing': listing})
# ====================== add_comment ====================================

@login_required
def add_comment(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        commenter = request.user
        Comment.objects.create(listing=listing, commenter=commenter, content=content)
    return redirect('listing_detail', listing_id=listing.id)
# ====================Login and register============================


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

# ==============================================

@login_required
def watchlist(request):
    if request.user.is_authenticated:
        watchlist_items = Watchlist.objects.get_or_create(user=request.user)[0].listings.all()
        return render(request, 'auctions/watchlist.html', {'watchlist_items': watchlist_items})
    else:
        return render(request, 'auctions/login_required.html')

@login_required
def add_to_watchlist(request, listing_id):
    if request.user.is_authenticated:
        listing = get_object_or_404(Listing, pk=listing_id)
        watchlist = Watchlist.objects.get_or_create(user=request.user)[0]
        watchlist.listings.add(listing)
        return redirect('watchlist')
    else:
        return render(request, 'auctions/login_required.html')

# def remove_from_watchlist(request, listing_id):
#     if request.user.is_authenticated:
#         listing = get_object_or_404(Listing, pk=listing_id)
#         watchlist = Watchlist.objects.get_or_create(user=request.user)[0]
#         watchlist.listings.remove(listing)
#         return redirect('watchlist')
#     else:
#         return render(request, 'auctions/login_required.html')

@login_required
def remove_from_watchlist(request, listing_id):
    if request.user.is_authenticated:
        listing = get_object_or_404(Listing, pk=listing_id)
        watchlist, created = Watchlist.objects.get_or_create(user=request.user)
        if listing in watchlist.listings.all():
            watchlist.listings.remove(listing)
            messages.success(request, f'Listing "{listing.title}" removed from your watchlist.')
        else:
            messages.warning(request, f'Listing "{listing.title}" is not in your watchlist.')
        return redirect('watchlist')
    else:
        return render(request, 'auctions/login_required.html')


def listing_detail(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    return render(request, 'auctions/listing_detail.html', {'listing': listing})

