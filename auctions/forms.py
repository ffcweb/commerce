from django import forms
from .models import Listing


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'starting_bid', 'category', 'is_active', 'url']

# class BidForm(forms.Form):
#     bid_amount = forms.DecimalField(
#         max_digits=10,
#         decimal_places=2,
#         label='Bid Amount',
#         widget=forms.NumberInput(attrs={'step': '0.01', 'min': '0.00'})
#     )
#
# class BidForm(forms.Form):
#     bid_amount = forms.DecimalField(label='Bid Amount', min_value=0.01, required=False)
class BidForm(forms.Form):
    bid_amount = forms.DecimalField(label='Bid Amount', max_digits=10, decimal_places=2)