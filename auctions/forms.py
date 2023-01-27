from django import forms
from .models import *

class ListingForm(forms.ModelForm):
    class Meta:
        model = Auction
        exclude = ('seller', 'is_active')
        widgets = {
            'description': forms.Textarea(attrs={'cols':50,'rows':10})
        }


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['price', 'edit_bid']
        widgets={
            'edit_bid': forms.HiddenInput
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment', 'edit_comment']
        widgets = {
            'comment': forms.Textarea(attrs={'cols':75,'rows':5}),
            'edit_comment': forms.HiddenInput
        }