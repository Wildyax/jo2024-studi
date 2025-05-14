from .utils import generate_secure_key, generate_qr_code, render_pdf
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from .session_persist import persist_session_vars
from user.models import CustomUser
from offer.models import Offer
from order.models import Order
from .forms import SubscribeForm, LoginForm, PaymentForm
from .cart import Cart

import stripe

"""
Home page route : /
"""
def index(request):
    return render(request, 'index.html', {})

"""
Offers page route : /offers
"""
def offers(request):
    offers = Offer.objects.all()
    return render(request, 'offers.html', {'offers': offers})

"""
Subscribe / Login page route : /subscribe
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
        if subscribe_form.is_valid():
            user = CustomUser.objects.create_user(
                email=subscribe_form.cleaned_data["email"],
                password=subscribe_form.cleaned_data["password"],
                last_name=subscribe_form.cleaned_data["name"],
                first_name=subscribe_form.cleaned_data["first_name"],
                userkey=generate_secure_key(16),
            )
            login(request, user)
            return redirect("payment")
    
    elif request.method == 'POST' and request.POST.get('form-name') == 'login':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(request, email=login_form.cleaned_data["email"], password=login_form.cleaned_data["password"])
            if user is not None and not user.is_staff:
                login(request, user)
                return redirect("index")
            else:
                login_form.add_error("password", "L'utilisateur n'existe pas ou le mot de passe est incorrect")
        else:
            login_form.add_error("password", "L'utilisateur n'existe pas ou le mot de passe est incorrect")

    return render(request, 'subscribe.html', {"subscribe_form": subscribe_form, "login_form": login_form, "form_name": form_name})

"""
Logout route : /logout
"""
@persist_session_vars(['cart'])
def log_out(request):
    logout(request)
    return redirect("index")

"""
Payment page route : /payment
"""
def payment(request):
    cart = Cart(request)
    if not request.user.is_authenticated or not cart.getOffer():
        return redirect('index')
    
    return render(request, 'payment.html', {'offer': cart.getOffer()})

"""
Order confirm page route : /order-confirm
"""
def order_confirm(request, order_id):
    if not order_id:
        return redirect('index')

    order = Order.objects.get(id=order_id)
    if not request.user.is_authenticated or order.user != request.user:
        return redirect('index')

    return render(request, 'order-confirm.html', {'order': order})

def order_fail(request):
    return render(request, 'order-fail.html')

"""
Ticket generation route : /generate-ticket
"""
def generate_ticket(request, order_id):
    if not order_id:
        return redirect('index')
    order = Order.objects.get(id=order_id)

    if not request.user.is_authenticated or order.user != request.user:
        return redirect('index')
    
    qr_data = f"{request.user.userkey}:{order.orderkey}"
    qr_code_b64 = generate_qr_code(qr_data)

    pdf = render_pdf('ticket.html', {'order': order, 'qr_code': qr_code_b64})

    return HttpResponse(pdf, content_type='application/pdf')

"""
Account page route : /account
"""
def account(request):
    if not request.user.is_authenticated:
        return redirect('index')
    
    orders = Order.objects.filter(user=request.user)
    
    return render(request, 'account.html', {'orders': orders})

"""
Ajax add to cart route : /add-to-cart
"""
@require_http_methods(["GET"])
def add_to_cart(request):
    cart = Cart(request)
    cart.add(request.GET.get('offer_id'))

    return JsonResponse({'success': True, 'cart': cart.cart})

"""
Ajax clear cart route : /clear-cart
"""
@require_http_methods(["GET"])
def clear_cart(request):
    cart = Cart(request)
    cart.clear()
   
    return JsonResponse({'success': True})

"""
Cart page route : /cart
"""
def show_cart(request):
    cart = Cart(request)    
    return render(request, 'cart.html', {'offer': cart.getOffer()})

"""
Stripe checkout url
"""
def create_checkout_session(request):
    cart = Cart(request)
    if not cart.getOffer():
        return redirect('index')
    
    stripe.api_key = settings.PRIVATE_STRIPE_KEY
    checkout_session = stripe.checkout.Session.create(
        line_items=[
            {
                'price_data': {
                    'currency': 'eur',
                    'product_data': {
                        'name': 'Offre ' + cart.getOffer().title,
                        'description': cart.getOffer().description,
                    },
                    'unit_amount': str(cart.getOffer().price).replace('.', '')
                },
                'quantity': 1
            }
        ],
        mode='payment',
        success_url=settings.DOMAIN_URL + '/success-checkout-session?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=settings.DOMAIN_URL + '/order-fail'
    )

    return redirect(checkout_session.url)

"""
Stripe success payment page
"""
def success_checkout_session(request):
    session_id = request.GET.get('session_id')
    cart = Cart(request)
    if not session_id or not cart.getOffer():
        return redirect('index')
    
    stripe.api_key = settings.PRIVATE_STRIPE_KEY
    session = stripe.checkout.Session.retrieve(session_id)

    if session.payment_status == 'paid':
        existing_order = Order.objects.filter(stripe_session_id=session_id).first()
        if existing_order:
            return redirect('order_confirm', order_id=str(existing_order.id))
        
        order = Order.objects.create(
            user = request.user,
            offer = cart.getOffer(),
            orderkey = generate_secure_key(16),
            stripe_session_id = session_id
        )

        cart.clear()
        return redirect('order_confirm', order_id=str(order.id))
    
    return redirect('order_fail')