# Generated by Django 3.1.7 on 2021-04-29 18:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('online_store', '0007_auto_20210429_1844'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Заказчик', 'verbose_name_plural': 'Заказчики'},
        ),
    ]