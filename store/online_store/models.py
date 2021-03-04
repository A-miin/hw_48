from django.db import models

# Create your models here.
CATEGORY_CHOICES=[
    ('breakfast','завтрак'),
    ('first meal','первые блюда'),
    ('second courses','вторые блюда'),
    ('the drinks','напитки '),
    ('other','разное')]

class Product(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name="Наименование")
    description = models.TextField(max_length=2000, null=True, blank=True, verbose_name="Описание")
    category = models.CharField(max_length=32, null=False, blank=False, choices=CATEGORY_CHOICES, default='other')
    remainder = models.IntegerField()
    price = models.FloatField()

    class Meta:
        db_table = 'products'
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return f'{self.id}. {self.name}: {self.price}'
