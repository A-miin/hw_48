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
        if self.kwargs.get('category'):
            queryset = queryset.filter(category=self.kwargs.get('category'))
        queryset = queryset.exclude(remainder=0)
        print('kwargs=',self.kwargs)

        if self.search_data:
            queryset = queryset.filter(
                Q(name__icontains=self.search_data) |
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

class ViewProductView(DetailView):
    template_name = 'product/view.html'
    queryset = Product.objects.exclude(remainder=0)
    context_object_name = 'product'

class CreateProductView(CreateView):
    template_name = 'product/create.html'
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        return reverse('product_view', kwargs={'pk': self.object.pk})

class UpdateProductView(UpdateView):
    form_class = ProductForm
    model = Product
    template_name = 'product/update.html'
    context_object_name = 'product'

    def get_success_url(self):
        return reverse('product_view', kwargs={'pk':self.object.pk})

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.exclude(remainder=0)
        return queryset

class DeleteProductView(DeleteView):
    template_name = 'product/delete.html'
    model = Product
    context_object_name = 'product'
    success_url = reverse_lazy('product_list')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.exclude(remainder=0)
        return queryset

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
