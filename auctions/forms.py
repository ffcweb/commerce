from django import forms
from .models import Listing
from django import forms

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'starting_bid', 'category', 'is_active', 'url']

class BidForm(forms.Form):
    bid_amount = forms.DecimalField(label='Bid Amount', max_digits=10, decimal_places=2)

class YourBidForm(forms.Form):
    bid_amount = forms.DecimalField(
        label='Bid Amount',
        min_value=0.01,  # Adjust as needed
        widget=forms.NumberInput(attrs={'step': '0.01'}),  # Optional: For decimal places
    )