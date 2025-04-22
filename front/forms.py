from django import forms
import re


class SubscribeForm(forms.Form):
    name = forms.CharField(
        label="Nom", 
        max_length=150, 
        required=True, 
        widget=forms.TextInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(
        label="Prénom", 
        max_length=150, 
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(
        label="E-mail",
        max_length=150, 
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(
        label="Mot de passe",
        max_length=128,
        min_length=8,
        required=True,
        help_text="Votre mot de passe doit contenir au moins 8 caractères, une lettre majuscule, un chiffre, et ne doit pas contenir d'espaces.",
        widget=forms.PasswordInput(attrs={"class": "form-control"}))
    
    def clean_password(self):
        password = self.cleaned_data.get("password")
        pattern = r'^(?=.*[A-Z])(?=.*\d)[^\s]{8,}$'

        if not re.match(pattern, password):
            raise forms.ValidationError(
                "Votre mot de passe doit contenir au moins 8 caractères, une lettre majuscule, un chiffre, et ne doit pas contenir d'espaces."
            )
        return password


class LoginForm(forms.Form):
    email = forms.EmailField(
        label="E-mail",
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(
        label="Mot de passe",
        required=True,
        widget=forms.PasswordInput(attrs={"class": "form-control"}))
    

class PaymentForm(forms.Form):
    code = forms.CharField(
        label="Code carte",
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "1234 5678 9876 5432"}))
    expire = forms.CharField(
        label="Expire",
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "01/12"}))
    security_code = forms.CharField(
        label="Code sécurité",
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "123"}))