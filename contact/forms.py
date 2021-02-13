from django import forms
from .models import UsersEmail


class UsersEmailForm(forms.ModelForm):
    """Форма подписки на рассылку"""

    class Meta:
        model = UsersEmail
        fields = ('email',)
        widgets = {
            'email': forms.TextInput(attrs={'class': 'editContent', 'placeholder': 'Your email...','name': 'email'})
        }
        labels = {
            'email': ''
        }
