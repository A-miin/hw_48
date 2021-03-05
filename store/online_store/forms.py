from django import forms

from .models import Product


# class ArticleForm(forms.ModelForm):
#     """
#     Форма для создания и редактирваония объектов статьи
#     https://docs.djangoproject.com/en/3.1/ref/forms/
#     """
#     class Meta:
#         model = Article
#         fields = ('title', 'content', 'author')

class ProductSearchForm(forms.Form):
    name = forms.CharField(max_length=100)