from django import forms

from .models import Product, Order
CATEGORY_CHOICES=[
    ('breakfast','завтрак'),
    ('first meal','первые блюда'),
    ('second courses','вторые блюда'),
    ('drinks','напитки '),
    ('other','разное'),
]

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('name', 'description', 'category', 'price', 'remainder')


class ProductSearchForm(forms.Form):
    name = forms.CharField(max_length=100)

class SearchForm(forms.Form):
    search_value = forms.CharField(max_length=100, required=False, label='Найти')

class OrderForm(forms.ModelForm):
    class Meta:
        model=Order
        fields=('name', 'tel', 'address')