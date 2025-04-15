from django.shortcuts import render
from django.contrib.auth import login, authenticate
from .forms import LoginForm

# Create your views here.
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
    