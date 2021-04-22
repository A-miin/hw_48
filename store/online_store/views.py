from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from django.utils.http import urlencode
from django.contrib import messages

from .forms import ProductSearchForm, ProductForm, SearchForm, OrderForm
from .models import Product, CATEGORY_CHOICES, CartProduct, ProductOrder, Order
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
        print(f'session={self.request.session.get("products",{})}')
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

class CreateProductView(PermissionRequiredMixin, CreateView):
    permission_required = ['online_store.add_product']
    template_name = 'product/create.html'
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        return reverse('product_view', kwargs={'pk': self.object.pk})

class UpdateProductView(PermissionRequiredMixin,UpdateView):
    permission_required = ['online_store.change_product']
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

class DeleteProductView(PermissionRequiredMixin, DeleteView):
    permission_required = ['online_store.delete_product']
    template_name = 'product/delete.html'
    model = Product
    context_object_name = 'product'
    success_url = reverse_lazy('product_list')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.exclude(remainder=0)
        return queryset


class AddToCartView(View):
    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product,id=kwargs.get('pk'))
        try:
            cart_product = CartProduct.objects.get(product=product)
            if product.remainder>0:
                cart_product.qty+=1
                product.remainder-=1
                product.save()
                cart_product.save()
                if 'products' not in request.session:
                    request.session['products'] = {}
                products = request.session.get('products', {})
                products[product.name] = cart_product.qty
                request.session['products'] = products
                messages.success(self.request, f'{product.name} : 1 item added')
            else:
                messages.error(self.request, f'Cannot add {product.name}')
        except CartProduct.DoesNotExist:
            if product.remainder!=0:
                cart_product=CartProduct.objects.create(product=product, qty=1)
                product.remainder -= 1
                product.save()
                if 'products' not in request.session:
                    request.session['products'] = {}
                products = request.session.get('products', {})
                products[product.name] = cart_product.qty
                request.session['products'] = products
                messages.success(self.request, f'{product.name} : 1 item added')
            else:
                messages.error(self.request, f'Cannot add {product.name}')


        return redirect('cart_list')

class IndexCartView(ListView):
    template_name = 'basket/index.html'
    model = CartProduct
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form']=OrderForm()
        return context


class DeleteCartView(DeleteView):
    model = CartProduct
    success_url = reverse_lazy('cart_list')
    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        product = Product.objects.get(id=self.object.product.id)
        product.remainder+=self.object.qty
        product.save()
        products = request.session.get('products', {})
        products[product.name] = None
        request.session['products'] = products
        self.request.session['products'][product.name] = None
        messages.warning(self.request, f'{product.name} deleted')
        self.object.delete()

        return HttpResponseRedirect(success_url)

class CreateOrderView(View):
    def post(self, request, *args, **kwargs):
        form = OrderForm(data=request.POST)
        if form.is_valid():
            order = Order.objects.create(
                name=form.cleaned_data.get('name'),
                tel=form.cleaned_data.get('tel'),
                address=form.cleaned_data.get('address')
            )
            for product in CartProduct.objects.all():
                product_order=ProductOrder.objects.create(order=order, product=product.product, qty=product.qty)
                product_order.save()

            CartProduct.objects.all().delete()
            return redirect('product_list')
        else:
            print(form.errors)
            print('errors')
            return redirect('cart_list')


