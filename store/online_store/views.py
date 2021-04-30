from copy import deepcopy

from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from django.utils.http import urlencode
from django.contrib import messages
from datetime import datetime, timedelta

from .forms import ProductSearchForm, ProductForm, SearchForm, OrderForm
from .models import Product, CATEGORY_CHOICES, CartProduct, ProductOrder, Order
# Create your views here.

class StatMixin:
    request = None

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.set_common_stat()
        self.set_page_time()
        return super().dispatch(request, *args, **kwargs)

    def set_common_stat(self):
        print(self.request.path)
        if 'stat' not in self.request.session:
            self.request.session['stat'] = {}

        stat = self.request.session.get('stat', {})
        if 'common_start_time' not in stat:
            stat['common_start_time'] = datetime.now().strftime('%d/%m/%y %H:%M:%S')
        if 'common_click_count' not in stat:
            stat['common_click_count'] = 1
        else:
            stat['common_click_count'] += 1
        self.request.session['stat'] = stat


    def set_page_time(self):
        if 'stat' not in self.request.session:
            self.request.session['stat'] = {}
        stat = self.request.session.get('stat', {})
        if 'page' not in stat.keys():
            stat['page']={}
        page=stat['page']
        if self.request.path not in page:
            page[self.request.path]={}
            page[self.request.path]['time'] = 0
            page[self.request.path]['click'] = 1
        else:
            page[self.request.path]['click'] +=1

        if 'new' in stat:
            old_time =page[stat['new']['path']]['time']
            time = (datetime.now() - datetime.strptime(stat['new']['start'], '%d/%m/%y %H:%M:%S')).seconds
            new_time = int(old_time) + time
            page[stat['new']['path']]['time'] = new_time
        else:
            stat['new']={}
        stat['new']['start'] = datetime.now().strftime('%d/%m/%y %H:%M:%S')
        stat['new']['path'] = self.request.path

        stat['page']=page
        self.request.session['stat'] = stat


class StatView(StatMixin, View):
    def get(self, request, *args, **kwargs):
        common_time = 0
        clicks=0
        if 'stat' not in self.request.session:
            self.request.session['stat'] = {}
        stat = self.request.session.get('stat', {})
        stat = deepcopy(stat)

        if 'common_start_time' in stat:
            start = datetime.strptime(stat['common_start_time'], '%d/%m/%y %H:%M:%S')
            end = datetime.now()
            common_time = str(end - start)
            clicks = stat['common_click_count']

        if 'page' not in stat:
            stat['page']={}
        pages=stat['page']
        print(f'pages={pages}')
        for key,values in pages.items():
            pages[key]['time'] = datetime.fromtimestamp(int(pages[key]['time'])).strftime("%H:%M:%S")

        if '/stat/' in pages:
            pages.pop('/stat/')

        print(f'pages={pages}')

        return render(request, 'stat.html', context={'time':common_time, 'cls':clicks, 'pages':pages})

class IndexProductView(StatMixin, ListView):
    template_name = 'product/index.html'
    model = Product
    context_object_name = 'products'
    ordering = ('category', 'name')
    paginate_by = 5


    def get(self,request, **kwargs):
        # self.set_time(request)
        self.form = SearchForm(request.GET)
        self.search_data = self.get_search_data()
        # print(f'session={self.request.session.get("products",{})}')
        print(f'session={self.request.session.get("stat",{})}')
        return super().get(request, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.kwargs.get('category'):
            queryset = queryset.filter(category=self.kwargs.get('category'))
        queryset = queryset.exclude(remainder=0)

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

class ViewProductView(StatMixin, DetailView):
    template_name = 'product/view.html'
    queryset = Product.objects.exclude(remainder=0)
    context_object_name = 'product'

class CreateProductView(PermissionRequiredMixin, StatMixin, CreateView):
    permission_required = ['online_store.add_product']
    template_name = 'product/create.html'
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        return reverse('product_view', kwargs={'pk': self.object.pk})

class UpdateProductView(PermissionRequiredMixin,StatMixin, UpdateView):
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

class DeleteProductView(PermissionRequiredMixin,StatMixin,  DeleteView):
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

class IndexCartView(StatMixin, ListView):
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
            if request.user.is_authenticated:
                order.user=request.user
                order.save()

            for product in CartProduct.objects.all():
                product_order=ProductOrder.objects.create(order=order, product=product.product, qty=product.qty)
                product_order.save()

            CartProduct.objects.all().delete()
            return redirect('product_list')
        else:
            print(form.errors)
            print('errors')
            return redirect('cart_list')



class UserOrderView(LoginRequiredMixin, StatMixin, ListView):
    template_name = 'product/user_orders.html'
    model = Order
    context_object_name = 'orders'

    def get_queryset(self):
        queryset = self.request.user.order.all().order_by('created_at')

        return queryset

