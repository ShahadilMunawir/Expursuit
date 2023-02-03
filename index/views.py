from django.shortcuts import render

# Create your views here.

def root_view(request):
    return render(request, 'index.html', context={})