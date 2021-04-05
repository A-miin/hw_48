from django.shortcuts import render
from .models import Product, CATEGORY_CHOICES
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from django.utils.http import urlencode

from .forms import ProductSearchForm, ProductForm, SearchForm
# Create your views here.
class IndexProductView(ListView):
    template_name = 'product/index.html'
    model = Product
    context_object_name = 'products'
    ordering = ('category', 'name')
    paginate_by = 5

    def get(self,request, **kwargs):
        self.form = SearchForm(request.GET)
        self.search_data = self.get_search_data()
        return super().get(request, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.exclude(remainder=0)

        if self.search_data:
            queryset = queryset.filter(
                Q(summary__icontains=self.search_data) |
                Q(description__icontains=self.search_data))
        return queryset

    def get_search_data(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search_value']
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = CATEGORY_CHOICES
        context['search_form'] = self.form

        if self.search_data:
            context['query'] = urlencode({'search_value': self.search_data})
        return context

def index(request):
    form = ProductSearchForm()
    if request.method=='GET':
        products = Product.objects.all().order_by('category', 'name').exclude(remainder=0)
        return render(request, 'product/index.html', context={'products':products, 'form':form, 'categories':CATEGORY_CHOICES})
    elif request.method=='POST':
        name = request.POST.get('name')
        products = Product.objects.all().filter(name=name).order_by('category', 'name').exclude(remainder=0)
        return render(request, 'product/index.html', context={'products':products, 'form':form, 'categories':CATEGORY_CHOICES})

def product_category_list(request, category):
    form = ProductSearchForm()
    if request.method=='GET':
        products = Product.objects.all().filter(category=category).order_by('name').exclude(remainder=0)
        return render(request, 'product/categories.html', context={'products':products, 'form':form, 'categories':CATEGORY_CHOICES})
    elif request.method=='POST':
        name = request.POST.get('name')
        products = Product.objects.all().filter(category=category, name=name).order_by('name').exclude(remainder=0)
        return render(request, 'product/categories.html', context={'products':products, 'form':form, 'categories':CATEGORY_CHOICES})

def product_view(request, pk):
    product = get_object_or_404(Product, id=pk)
    return render(request, 'product/view.html', {'product':product})

def product_create(request):
    if request.method=='GET':
        form = ProductForm()
        return render(request, 'product/create.html', {'form':form})
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
            return render(request, 'product/create.html', context={'form':form})

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
        return render(request, 'product/update.html', context={'form':form, 'product':product})
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
            return render(request, 'product/update.html', context={'form':form, 'product':product})

def product_delete(request, pk):
    product = get_object_or_404(Product, id=pk)
    if request.method=='GET':
        return render(request, 'product/delete.html', context={'product':product})
    elif request.method=='POST':
        if request.POST.get('action')=='Да':
            product.delete()
            return redirect('product_list')
        else:
            return redirect('product_view', product.id)
