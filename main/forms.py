from django import forms
from .models import Review, Rating, RatingStar


class ReviewForm(forms.ModelForm):
    """Форма добавления отзывов"""

    class Meta:
        model = Review
        fields = ('name', 'email', 'text')


class RatingForm(forms.ModelForm):
    """Форма добавления рейтинга"""
    stars = forms.ModelChoiceField(
        queryset=RatingStar.objects.all(), widget=forms.RadioSelect(), empty_label=None
    )

    class Meta:
        model = Rating
        fields = ('stars',)



