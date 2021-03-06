# Generated by Django 3.1.7 on 2021-03-08 12:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online_store', '0002_auto_20210305_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=9),
        ),
        migrations.AlterField(
            model_name='product',
            name='remainder',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
