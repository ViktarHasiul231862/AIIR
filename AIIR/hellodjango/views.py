from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

def show(request):
    return HttpResponse("Hello DJANGO!!!")