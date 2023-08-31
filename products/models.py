from django.db import models
from django.urls import reverse
from slugify import slugify

# Create your models here.

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
    slug = models.SlugField(max_length=148, unique=True, verbose_name='URL-имя')
    is_available = models.BooleanField(default=True, verbose_name='Доступность товара')
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата добавления товара')
    image = models.ImageField(upload_to='images/', verbose_name='Изображение товара')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, verbose_name='Подкатегория')

    class Meta:
       verbose_name = 'Товар'
       verbose_name_plural = 'Товары'
       ordering = ['name', '-price']

    def get_url(self):
        return reverse('product_datail', args=[self.category.slug, self.slug])

    def __str__(self) -> str:
        return self.name



