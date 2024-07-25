from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User







class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    



class StripePaymentForm(forms.Form):
    stripe_token = forms.CharField()
    
    
class FakePaymentForm(forms.Form):
    card_number = forms.CharField(max_length=16, required=True, widget=forms.TextInput(attrs={'placeholder': 'Card Number'}))
    expiry_date = forms.CharField(max_length=5, required=True, widget=forms.TextInput(attrs={'placeholder': 'MM/YY'}))
    cvv = forms.CharField(max_length=3, required=True, widget=forms.TextInput(attrs={'placeholder': 'CVV'}))