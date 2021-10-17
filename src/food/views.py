from django.shortcuts import render

# Create your views here.
def home(request):
    context = {}
    return render(request, 'food/home.html', context)

def menu(request):
    context = {}
    return render(request, 'food/menu.html', context)