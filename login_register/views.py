from django.shortcuts import render

# Create your views here.

def login_view(request):
    return render(request, 'login.html', context={})

def signup_view(request):
    return render(request, 'signup.html', context={})

def reset_password_view(request):
    return render(request, 'reset_password.html', context={})

def home_view(request):
    spending = 10000
    budget = 20000
    percentage = int((spending/budget)*100)
    context = {
        "name": "Shahadil Munawir",
        "spending": 10000,
        "budget": 20000,
        "percentage": percentage
    }
    return render(request, 'home.html', context=context)