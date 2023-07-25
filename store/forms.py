from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product



class NewUserForm(UserCreationForm):
    username = forms.CharField(label='',required=True, widget=forms.TextInput(attrs={'class':'form-control my-3','placeholder':'Username'}))
    email = forms.EmailField(label='',required=True, widget=forms.EmailInput(attrs={'class':'form-control my-3','placeholder':'Email'}))
    password1 = forms.CharField(label='',required=True, widget=forms.PasswordInput(attrs={'class':'form-control my-3','placeholder':'Password'}))
    password2 = forms.CharField(label='',required=True, widget=forms.PasswordInput(attrs={'class':'form-control my-3','placeholder':'Confirm Password'}))

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2',
        )



class ProductForm(forms.ModelForm):
    name = forms.CharField(label='',required=True, widget=forms.TextInput(attrs={'class':'form-control my-3','placeholder':'Name'}))
    description = forms.CharField(label='',required=True, widget=forms.Textarea(attrs={'class':'form-control my-3','placeholder':'Description'}))
    price = forms.IntegerField(label='', required=True, widget=forms.NumberInput(attrs={'class':'form-control my-3','placeholder':'Price'}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'accept': 'image/*'}))

    class Meta:
        model = Product
        fields = (
            'name',
            'description',
            'price',
            'image',
        )
