from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):
    domain = request.GET.get('dominio')

    return HttpResponse("Your domain: " + ('' if domain is None else domain) + "\nHello, world.")
