from django.shortcuts import render
from .models import Product
# Create your views here.
def index(request):
    products = Product.objects.all().order_by('category', 'name')
    return render(request,'index.html', context={'products':products})