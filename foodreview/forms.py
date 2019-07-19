from django import forms
from foodreview.models import Restaurant, Review, Like, Region

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('comment',)