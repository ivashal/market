from django.db import models
from django.urls import reverse
from slugify import slugify
import os

# Create your models here.

def create_directory_path(instance, filename):  ## Обычно instance называют создание нового объекта
    filename = os.path.join('images', instance.category.slug, instance.subcategory.slug)
    return filename
    # return f'images/{instance.category.slug}/{instance.subcategory.slug}'  ## Пример без join

class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя категории', unique=True)
    description = models.TextField(max_length=1000, verbose_name='Описание категории')
    slug = models.SlugField(max_length=256, unique=True, verbose_name='URL-имя', editable=False)  # отображает имя сущности

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name',]

    def __str__(self) -> str:
        return self.name

        
    def save(self, *args, **kwargs):  ## Выполняется в тот момент когда мы создаем строчку в таблице
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)  ## Для применения изменений в родительский класс


class SubCategory(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Имя подкатегории')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Категория', related_name='categories')  ## elated_name='category' - имя связи
    slug = models.SlugField(max_length=70, unique=True, verbose_name='URL-имя', editable=False)  ## Эдитейбл - возможность релактировать

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'
        ordering = ['name',]

    def save(self, *args, **kwargs):  ## Выполняется в тот момент когда мы создаем строчку в таблице
        self.slug = slugify(self.name)
        super(SubCategory, self).save(*args, **kwargs)  ## Для применения изменений в родительский класс

    def get_absolute_url(self):  # Используется для получения URL возвращает страничку
        return reverse('products:product-list',kwargs={'cat_slug': self.category.slug, 'subcat_slug': self.slug})  # передает имя продукта


class Products(models.Model):
    name = models.CharField(max_length=128, unique=True, verbose_name='Название товара')
    description = models.TextField(max_length=1000, verbose_name='Описание товара')
    price = models.FloatField(verbose_name='Цена товара')
    slug = models.SlugField(max_length=148, unique=True, verbose_name='URL-имя',editable=False)
    is_available = models.BooleanField(default=True, verbose_name='Доступность товара')
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата добавления товара')
    image = models.ImageField(upload_to=create_directory_path, verbose_name='Изображение товара', null=True, blank=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.PROTECT, verbose_name='Подкатегория',editable=False, related_name='subcategory')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Категория', editable=False, related_name='category')


    class Meta:
       verbose_name = 'Товар'
       verbose_name_plural = 'Товары'
       ordering = ['name', '-price']

    def get_absolute_url(self):
        return reverse('products:product-detail', kwargs={
            'cat_slug':self.category.slug,
            'subcat_slug': self.subcategory.slug,
            'prod_slug': self.slug
            }
        )

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):  ## Выполняется в тот момент когда мы создаем строчку в таблице
        self.slug = slugify(self.name)  ## транслитирирует название
        super(Products, self).save(*args, **kwargs)  ## Для применения изменений в родительский класс


