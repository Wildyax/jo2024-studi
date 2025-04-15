from django import forms 

class LoginForm(forms.Form):
    email = forms.EmailField(
        label="E-mail",
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(
        label="Mot de passe",
        required=True,
        widget=forms.PasswordInput(attrs={"class": "form-control"}))