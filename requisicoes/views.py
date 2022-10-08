from django.shortcuts import render
from django.conf import settings

def index(request):
    context = {} 
    return render(request, 'index.html', context)
