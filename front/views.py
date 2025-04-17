from .utils import generateUserKey
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from .session_persist import persist_session_vars
from user.models import CustomUser
from offer.models import Offer
from .forms import SubscribeForm, LoginForm
from .cart import Cart

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
@persist_session_vars(['cart'])
def subscribe(request):
    
    if request.user.is_authenticated:
        return redirect('index')
    
    subscribe_form = SubscribeForm()
    login_form = LoginForm()
    form_name = request.POST.get('form-name') if request.POST.get('form-name') else ""
    form_name = request.GET.get('form-name') if  request.GET.get('form-name') else form_name

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
@persist_session_vars(['cart'])
def logOut(request):
    logout(request)
    return redirect("index")

"""
Route vers la page de paiement : /payment
"""
def payment(request):
    cart = Cart(request)

    if not request.user.is_authenticated or not cart.getOffer():
        return redirect('index.html')
    
    if request.method == 'POST':
        pass
    
    return render(request, 'payment.html', {'offer': cart.getOffer()})

"""
Route pour ajouter au panier : /add-to-cart
"""
@require_http_methods(["GET"])
def addToCart(request):
    cart = Cart(request)
    cart.add(request.GET.get('offer_id'))

    return JsonResponse({'success': True, 'cart': cart.cart})

"""
Route pour vider le panier : /clear-cart
"""
@require_http_methods(["GET"])
def clearCart(request):
    cart = Cart(request)
    cart.clear()
   
    return JsonResponse({'success': True})

"""
Route pour afficher le panier : /cart
"""
def showCart(request):
    cart = Cart(request)    
    return render(request, 'cart.html', {'offer': cart.getOffer()})