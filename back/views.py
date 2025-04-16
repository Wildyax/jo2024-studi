from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login, authenticate
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseNotAllowed, HttpResponse, JsonResponse
from django.template.loader import render_to_string
from .forms import LoginForm
from offer.models import Offer
from offer.forms import OfferForm

# Create your views here.

"""
Route de la page d'accueil du Back-Office : back-office/
"""
def backOffice(request):
    login_form = LoginForm()

    if request.user.is_authenticated and request.user.is_staff:
        return render(request, 'back/back-office.html', {})
    
    elif request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(request, email=login_form.cleaned_data["email"], password=login_form.cleaned_data["password"])
            if user is not None and user.is_staff:
                login(request, user)
                return render(request, 'back/back-office.html', {})
            else:
                login_form.add_error("password", "Le mail n'existe pas ou le mot de passe est incorrect")
        else:
            login_form.add_error("password", "Le mail n'existe pas ou le mot de passe est incorrect")
        
    return render(request, 'back/login.html', {"login_form": login_form})
    
"""
Route de la page d'édition des offres : back-office/offers
"""
def offers(request):
    if request.user.is_authenticated and request.user.is_staff:
        offers_list = Offer.objects.all()
        return render(request, 'back/offers.html', {'offers': offers_list})
    
    return HttpResponseNotAllowed()

"""
Route Ajax du formulaire d'édition des offres : back-office/offers/edit
"""
@require_http_methods(["GET"])
def editOffer(request):
    if request.user.is_authenticated and request.user.is_staff:
        offer_id = request.GET.get('offer-id')
        offer_form = OfferForm()

        if offer_id is not None:
            offer_id = int(offer_id)
            if offer_id < 1:
                return render(request, 'back/partials/offers_edit.html', {'offer_form': offer_form, 'offer_id': offer_id})
            else:
                offer = get_object_or_404(Offer, id=offer_id)
                offer_form = OfferForm(instance=offer)
                return render(request, 'back/partials/offers_edit.html', {'offer_form': offer_form, 'offer_id': offer_id})

    return HttpResponseNotAllowed()

"""
Route Ajax de la sauvegarde du formulaire d'édition des offres : back-office/offers/edit
"""
@require_http_methods(["POST"])
def saveOffer(request):
    if request.user.is_authenticated and request.user.is_staff:
        offer_id = request.POST.get('offer-id')

        if int(offer_id) < 1:
            offer_form = OfferForm(request.POST, request.FILES)

            if offer_form.is_valid():
                offer = offer_form.save()
                offer_card = render_to_string('back/partials/offer_card.html', {'offer': offer}, request)
                return JsonResponse({'success': True, 'card_html': offer_card, 'offer_id': offer.id, 'new': True})
            else:
                return JsonResponse({'success': False})
        
        else:
            offer_instance = get_object_or_404(Offer, id=offer_id)
            offer_form = OfferForm(request.POST, request.FILES, instance=offer_instance)
            
            if offer_form.is_valid():
                offer = offer_form.save()
                offer_card = render_to_string('back/partials/offer_card.html', {'offer': offer}, request)
                return JsonResponse({'success': True, 'card_html': offer_card, 'offer_id': offer.id, 'new': False})
            else:
                return JsonResponse({'success': False})

    return HttpResponseNotAllowed()

"""
Route Ajax de la suppression d'une offre : back-office/offers/delete
"""
@require_http_methods(["GET"])
def deleteOffer(request):
    if request.user.is_authenticated and request.user.is_staff:
        offer_id = request.GET.get('offer-id')
        offer_instance = get_object_or_404(Offer, id=offer_id)
        offer_instance.delete()
        return JsonResponse({'success': True})

    return HttpResponseNotAllowed()