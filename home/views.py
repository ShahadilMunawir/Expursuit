from django.shortcuts import render

# Create your views here.

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