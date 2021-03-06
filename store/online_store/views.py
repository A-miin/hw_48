from django.shortcuts import render
from .models import Product
from django.shortcuts import get_object_or_404, redirect

from .forms import ProductSearchForm, ProductForm
# Create your views here.
def index(request):
    form = ProductSearchForm()
    if request.method=='GET':
        products = Product.objects.all().order_by('category', 'name')
        return render(request,'index.html', context={'products':products, 'form':form})
    elif request.method=='POST':
        print(request.POST)
        name = request.POST.get('name')
        products = Product.objects.all().filter(name=name).order_by('category', 'name')
        return render(request, 'index.html', context={'products':products, 'form':form})

def product_view(request, pk):
    product = get_object_or_404(Product, id=pk)
    return render(request, 'product_view.html', {'product':product})

def product_create(request):
    if request.method=='GET':
        form = ProductForm()
        return render(request, 'product_create.html', {'form':form})
    elif request.method=='POST':
        form = ProductForm(data=request.POST)
        if form.is_valid():
            product = Product.objects.create(
                name=form.cleaned_data.get('name'),
                category=form.cleaned_data.get('category'),
                description=form.cleaned_data.get('description'),
                remainder=form.cleaned_data.get('remainder'),
                price=form.cleaned_data.get('price')
            )
            return redirect('product_view',product.id)
        else:
            return render(request, 'product_create.html', context={'form':form})

def product_update(request, pk):
    product = get_object_or_404(Product, id=pk)
    if request.method=='GET':
        form = ProductForm(
            initial={
                'name':product.name,
                'category':product.category,
                'description':product.description,
                'remainder':product.remainder,
                'price':product.price
            }
        )
        return render(request,'product_update.html',context={'form':form, 'product':product})
    elif request.method=='POST':
        form=ProductForm(data=request.POST)
        if form.is_valid():
            product.name = form.cleaned_data.get('name')
            product.category = form.cleaned_data.get('category')
            product.description = form.cleaned_data.get('description')
            product.remainder = form.cleaned_data.get('remainder')
            product.price = form.cleaned_data.get('price')
            product.save()
            return redirect('product_view', product.id)
        else:
            return render(request, 'product_update.html', context={'form':form, 'product':product})

def product_delete(request, pk):
    product = get_object_or_404(Product, id=pk)
    if request.method=='GET':
        return render(request, 'product_delete.html', context={'product':product})
    elif request.method=='POST':
        if request.POST.get('action')=='Да':
            product.delete()
            return redirect('product_list')
        else:
            return redirect('product_view', product.id)
