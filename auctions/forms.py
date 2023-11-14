from django import forms
from .models import Listing


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'starting_bid', 'category', 'is_active', 'url']

class BidForm(forms.Form):
    bid_amount = forms.DecimalField(label='Bid Amount', max_digits=10, decimal_places=2)