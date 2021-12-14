from django.db import models
from rest_framework.exceptions import APIException

from login.models import UserProfile


class Product(models.Model):
    """
    Модель продукта
    """
    name = models.CharField(verbose_name='Наименование продукта', max_length=300)
    price = models.FloatField(verbose_name='Цена товара')
    creation_date = models.DateTimeField(verbose_name='Дата добавления продукта', auto_now=True)
    quantity = models.PositiveIntegerField(verbose_name='Количество товара', default=1)
    discount = models.FloatField(verbose_name='Скидка на товар', default=0)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return f'{self.name}, {self.price}₽, ({self.quantity}шт.)'


class Order(models.Model):
    """
    Модель заказа
    """
    STATUS_GENERATED = 1
    STATUS_DONE = 2
    STATUS_PAY = 3
    STATUS_CANCELLED = 4

    STATUSES = (
        (STATUS_GENERATED, 'Создан'),
        (STATUS_DONE, 'Выполнен'),
        (STATUS_PAY, 'Оплачен'),
        (STATUS_CANCELLED, 'Отменен')
    )
    DEFAULT_COUNT_PRODUCT = 1  # Кол-во товаров в заказе

    product = models.ForeignKey(Product, verbose_name='Продукт', on_delete=models.SET_NULL, null=True)
    status = models.PositiveSmallIntegerField(verbose_name='Статус', choices=STATUSES, default=STATUS_GENERATED)
    total_price = models.FloatField(verbose_name='Общая стоимость заказа', null=True)
    creation_date = models.DateTimeField(verbose_name='Дата создания заказа', auto_now=True)
    discount = models.FloatField(verbose_name='Общая скидка в заказе', default=0)
    session_key = models.CharField(verbose_name='Сессия анонимного пользователя', blank=True, max_length=1000)
    user = models.ForeignKey(UserProfile, verbose_name='Пользователь', null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'{self.pk}-{self.product}-{self.status}'


    def is_allowed_change_of_status(self, user_type):
        """
        Метод возвращающий список доступных статусов заказа для сотрудника
        """
        allowed_statuses_for_emploees = {
            UserProfile.TYPE_SELLER: (Order.STATUS_GENERATED, Order.STATUS_DONE),
            UserProfile.TYPE_CHECKER: (Order.STATUS_DONE, Order.STATUS_PAY)
        }
        return allowed_statuses_for_emploees.get(user_type, [])

    def save(self, *args, **kwargs):
        self.total_price = self.product.price * self.DEFAULT_COUNT_PRODUCT
        self.discount = self.product.discount * self.DEFAULT_COUNT_PRODUCT

        # Нельзя менять статус если пользователь неизвестен
        if self.user is None and self.status != self.STATUS_GENERATED:
            self.status = self.STATUS_GENERATED

        super().save()

    def delete(self, *args, **kwargs):
        if self.product is not None:
            self.product.quantity += self.DEFAULT_COUNT_PRODUCT
            self.product.save(update_fields=['quantity'])
        super().delete(*args, **kwargs)


class Score(models.Model):
    """
    Модель счета
    """
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(verbose_name='Дата создания счета', auto_now=True)

    class Meta:
        verbose_name = 'Счет'
        verbose_name_plural = 'Счета'

    def __str__(self):
        return f'{self.pk}-{self.order.product.name}-{self.order.user.email}'


class OrderPayments(models.Model):
    """
    Модель оплаты заказа
    """
    # TODO  сделать счет уникальным, оплата только по одному счету
    score = models.OneToOneField(Score, verbose_name='Счет', on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey(UserProfile, verbose_name='Покупатель', on_delete=models.SET_NULL, null=True)
    payment = models.FloatField(verbose_name='Оплата', default=0)

    def save(self, *args, **kwargs):
        if self.score.order.total_price <= self.payment:
            super().save(*args, **kwargs)
        else:
            raise APIException('Не хватает средств')

    def __str__(self):
        return f'{self.id}{self.order}'


class UserCart(models.Model):
    """
    Модель корзины пользователя
    """
    product = models.ForeignKey(Product, verbose_name='Продукт', on_delete=models.CASCADE, related_name='cart')
    creation_date = models.DateTimeField(verbose_name='Дата создания корзины', auto_now=True)
    session_key = models.CharField(verbose_name='Сессия анонимного пользователя', blank=True, max_length=1000)
    customer = models.ForeignKey(UserProfile, verbose_name='Покупатель', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.pk}-{self.product.name}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'




