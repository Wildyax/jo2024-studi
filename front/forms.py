from django import forms


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
        max_length=20,
        min_length=8,
        required=True,
        help_text="Votre mot de passe doit être compris entre 8 et 20 caractères, ne pas avoir d'espaces et contenir au moins un chiffre.",
        widget=forms.PasswordInput(attrs={"class": "form-control", "pattern": "^(?=\S{8,20}$)(?=.*\d).*$"}))
    
    def checkForm(self):
        if not self.checkPassword:
            return False
        return True

    def checkPassword(self, password: str):
        no_error = True
        
        if len(password) < 8 or len(password) > 20:
            self.add_error('password', 'Le mot de passe doit être compris entre 8 et 20 caractères')
            no_error = False
        if not any(char.isdigit() for char in password):
            self.add_error('password', 'Le mot de passe doit contenir un chiffre')
            no_error = False
        if password.count(' ') > 0:
             self.add_error('password', 'Le mot de passe ne doit pas contenir d\'espaces')
             no_error = False
        
        return no_error


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