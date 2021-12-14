from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser
)


class MyUserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None):
        user = self.create_user(
            email,
            password=password,
            full_name=full_name
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser):
    """
    Кастомная модель пользователя
    """
    TYPE_SELLER = 1
    TYPE_CHECKER = 2
    TYPE_BOOKKEEPER = 3
    TYPE_SHOPPER = 4

    TYPES_USER = (
        (TYPE_SELLER, 'Продавец-консультант'),
        (TYPE_CHECKER, 'Кассир'),
        (TYPE_BOOKKEEPER, 'Бухгалтер'),
        (TYPE_SHOPPER, 'Покупатель'),
    )

    email = models.EmailField(verbose_name='Почта', max_length=255, unique=True,)
    full_name = models.CharField(verbose_name='Полное имя', max_length=300)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    type_user = models.IntegerField(verbose_name='Тип пользователя', choices=TYPES_USER, default=TYPE_SHOPPER)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    objects = MyUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.get_type_user_display()} | {self.email}'

    @property
    def is_store_employee(self):
        return bool(self.type_user in (
            UserProfile.TYPE_SELLER,
            UserProfile.TYPE_CHECKER,
            UserProfile.TYPE_BOOKKEEPER
        ))

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin