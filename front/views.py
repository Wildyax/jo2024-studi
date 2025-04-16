from .utils import generateUserKey
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from user.models import CustomUser
from .forms import SubscribeForm, LoginForm
from offer.models import Offer

"""
Route de la page d'accueil : /
"""
def index(request):
    return render(request, 'index.html', {})

"""
Route de la page des offres : /offers
"""
def offers(request):
    offers = Offer.objects.all()
    return render(request, 'offers.html', {'offers': offers})

"""
Route de la page d'inscription || connexion : /subscribe
"""
def subscribe(request):
    
    if request.user.is_authenticated:
        return redirect('index')
    
    subscribe_form = SubscribeForm()
    login_form = LoginForm()
    form_name = request.POST.get('form-name') if request.POST.get('form-name') else "" 

    if request.method == 'POST' and request.POST.get('form-name') == 'subscribe':
        subscribe_form = SubscribeForm(request.POST)
        if subscribe_form.is_valid() and subscribe_form.checkForm():
            user = CustomUser.objects.create_user(
                email=subscribe_form.cleaned_data["email"],
                password=subscribe_form.cleaned_data["password"],
                last_name=subscribe_form.cleaned_data["name"],
                first_name=subscribe_form.cleaned_data["first_name"],
                userkey=generateUserKey(16),
            )
            login(request, user)
            return redirect("index")
    
    elif request.method == 'POST' and request.POST.get('form-name') == 'login':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(request, email=login_form.cleaned_data["email"], password=login_form.cleaned_data["password"])
            if user is not None and not user.is_staff:
                login(request, user)
                return redirect("index")
            else:
                login_form.add_error("password", "Le mail n'existe pas ou le mot de passe est incorrect")
        else:
            login_form.add_error("password", "Le mail n'existe pas ou le mot de passe est incorrect")

    return render(request, 'subscribe.html', {"subscribe_form": subscribe_form, "login_form": login_form, "form_name": form_name})

"""
Route pour la déconnexion : /logout
"""
def logOut(request):
    logout(request)
    return redirect("index")