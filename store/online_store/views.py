from django.shortcuts import render
from .models import Product
from django.shortcuts import get_object_or_404, redirect

from .forms import ProductSearchForm
# Create your views here.
def index(request):
    form = ProductSearchForm()
    if request.method=='GET':
        products = Product.objects.all().order_by('category', 'name')
        return render(request,'index.html', context={'products':products, 'form':form})
    elif request.method=='POST':
        print(request.POST)
        name = request.POST.get('name')
        product = get_object_or_404(Product,name=name)
        return render(request, 'index.html', context={'product':product, 'form':form})

def product_view(request, pk):
    product = get_object_or_404(Product, id=pk)
    return render(request, 'product_view.html', {'product':product})
