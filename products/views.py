from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse('This is page PRODUCTS')

def root_index(request):
    return HttpResponse('This is page MAIN')


