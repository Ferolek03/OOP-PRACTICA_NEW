from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
from django.utils.crypto import get_random_string

from catalog.utilities import get_timestamp_path


def get_name_file(instanse, filename):
    return '/'.join([get_random_string(length=5) + '_' + filename])


class User(AbstractUser):
    name = models.CharField(max_length=254, verbose_name='Имя', blank=False)
    surname = models.CharField(max_length=254, verbose_name='Фамилия', blank=False)
    patronymic = models.CharField(max_length=254, verbose_name='Отчество', blank=True)
    username = models.CharField(max_length=254, verbose_name='Логин', unique=True, blank=False)
    email = models.CharField(max_length=254, verbose_name='Почта', unique=True, blank=False)
    password = models.CharField(max_length=254, verbose_name='Пароль', blank=False)
    role = models.CharField(max_length=254, verbose_name='Роль',
                            choices=(('admin', 'Администратор'), ('user', 'Пользователь'), ('author', 'Автор')), default='user')



    def full_name(self):
        return ' '.join([self.name, self.surname, self.patronymic])

    def __str__(self):
        return self.full_name()


# Категория заявок
class Category(models.Model):
    name = models.CharField(max_length=254, verbose_name='Наименование', blank=False)

    def __str__(self):
        return self.name



class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('confirmed', 'Принято в работу'),
        ('canceled', 'Выполнено')
    ]
    date = models.DateTimeField(verbose_name='Дата заявки', auto_now_add=True)
    name = models.CharField(max_length=254, verbose_name='Имя', blank=False)
    status = models.CharField(max_length=254, verbose_name='Статус',
                              choices=STATUS_CHOICES,
                              default='new')
    photo_file = models.ImageField(max_length=254, upload_to=get_timestamp_path,
                                   blank=True, null=True,
                                   validators=[
                                       FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'bmp'])])
    category = models.ForeignKey('Category', verbose_name='Категория', on_delete=models.CASCADE)
    descriptions = models.TextField(verbose_name='описание', blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор объявления')
    imageses = models.ImageField(default='', blank=True, upload_to=get_timestamp_path, verbose_name=' Доп Изображение')
    commented = models.TextField(default='', verbose_name='Комментарий')
    counter = models.IntegerField(null=True, blank=True, verbose_name='счетчик')

    def count_product(self):
        count = 0
        for item_order in self.iteminorder_set.all():
            count += item_order.count
        return count

    def status_verbose(self):
        return dict(self.STATUS_CHOICES)[self.status]

    def __str__(self):
        return self.date.ctime() + ' | ' + self.user.full_name() + ' |  ' + str(self.count_product())

    def get_absolute_url(self):
        return reverse('product', args=[str(self.id)])

    def __str__(self):
        return self.name


class ItemInOrder(models.Model):
    order = models.ForeignKey(Order, verbose_name='Заявка', on_delete=models.CASCADE)
    count = models.IntegerField(verbose_name='Количество', blank=False, default=0)
