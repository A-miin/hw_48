from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
CATEGORY_CHOICES=[
    ('breakfast','завтрак'),
    ('first meal','первые блюда'),
    ('second courses','вторые блюда'),
    ('drinks','напитки '),
    ('other','разное'),
]

class Product(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name="Наименование")
    description = models.TextField(max_length=2000, null=True, blank=True, verbose_name="Описание")
    category = models.CharField(max_length=32, null=False, blank=False, choices=CATEGORY_CHOICES, default='other')
    remainder = models.IntegerField(validators=[MinValueValidator(0)])
    price = models.DecimalField(max_digits=9, decimal_places=2, validators=[MinValueValidator(0)])

    class Meta:
        db_table = 'products'
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return f'{self.id}. {self.name}: {self.price}'

class CartProduct(models.Model):
    product = models.ForeignKey('online_store.Product', on_delete=models.CASCADE, related_name='cart_products', verbose_name='продукт')
    qty = models.IntegerField(validators=[MinValueValidator(0)])

    class Meta:
        verbose_name="товар в корзине"
        verbose_name_plural="товары в корзине"

    def summa(self):
        return self.product.price*self.qty

    def get_all(self):
        summa=0
        for obj in CartProduct.objects.all():
            summa+=obj.summa()

        return summa

class Order(models.Model):
    name = models.CharField(max_length=128)
    tel = models.CharField(max_length=128)
    address = models.CharField(max_length=256)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ProductOrder(models.Model):
    product = models.ForeignKey('online_store.Product', on_delete=models.CASCADE, related_name='orders')
    order = models.ForeignKey('online_store.Order', on_delete=models.CASCADE, related_name='products')
    qty = models.IntegerField(validators=[MinValueValidator(0)])

    class Meta:
        verbose_name='Заказ'
        verbose_name_plural='Заказы'

    def __str__(self):
        return f'{self.order.name}:{self.product.name}-{self.qty}'