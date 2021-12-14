# Generated by Django 3.2.9 on 2021-12-07 19:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'Создан'), (2, 'Выполнен'), (3, 'Оплачен'), (4, 'Отменен')], default=1, verbose_name='Статус')),
                ('total_price', models.FloatField(null=True, verbose_name='Общая стоимость заказа')),
                ('creation_date', models.DateTimeField(auto_now=True, verbose_name='Дата создания заказа')),
                ('discount', models.FloatField(default=0, verbose_name='Общая скидка в заказе')),
                ('session_key', models.CharField(blank=True, max_length=1000, verbose_name='Сессия анонимного пользователя')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, verbose_name='Наименование продукта')),
                ('price', models.FloatField(verbose_name='Цена товара')),
                ('creation_date', models.DateTimeField(auto_now=True, verbose_name='Дата добавления продукта')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Количество товара')),
                ('discount', models.FloatField(default=0, verbose_name='Скидка на товар')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
            },
        ),
        migrations.CreateModel(
            name='UserCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now=True, verbose_name='Дата создания корзины')),
                ('session_key', models.CharField(blank=True, max_length=1000, verbose_name='Сессия анонимного пользователя')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Покупатель')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product', verbose_name='Продукт')),
            ],
            options={
                'verbose_name': 'Корзина',
                'verbose_name_plural': 'Корзины',
            },
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now=True, verbose_name='Дата создания счета')),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='products.order')),
            ],
            options={
                'verbose_name': 'Счет',
                'verbose_name_plural': 'Счета',
            },
        ),
        migrations.CreateModel(
            name='OrderPayments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment', models.FloatField(default=0, verbose_name='Оплата')),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Покупатель')),
                ('score', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.score', verbose_name='Счет')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.product', verbose_name='Продукт'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
