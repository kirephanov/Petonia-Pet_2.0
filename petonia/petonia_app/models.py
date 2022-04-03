from django.db import models

class Marker(models.Model):
    search = models.ForeignKey('Search', on_delete=models.PROTECT, null=True, verbose_name='Категория')
    animal = models.ForeignKey('Animal', on_delete=models.PROTECT, null=True, verbose_name='Животное')
    name = models.CharField(max_length=150, verbose_name='Имя')
    telephone = models.CharField(max_length=16, verbose_name='Телефон')
    street = models.CharField(max_length=150, verbose_name='Улица/Место')
    city = models.CharField(max_length=100, verbose_name='Город')
    region = models.ForeignKey('Region', on_delete=models.PROTECT, null=True, verbose_name='Область')
    country = models.CharField(max_length=100, verbose_name='Страна')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Фото', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    views = models.IntegerField(default=0, verbose_name='Просмотры')

    def __str__(self):
        return self.street

    class Meta:
        verbose_name = 'Метка'
        verbose_name_plural = 'Метки'
        ordering = ['-created_at']

class Region(models.Model):
    reg_name = models.CharField(max_length=50, db_index=True, verbose_name='Название области')

    def __str__(self):
        return self.reg_name

    class Meta:
        verbose_name = 'Область'
        verbose_name_plural = 'Области'
        ordering = ['reg_name']

class Animal(models.Model):
    animal_name = models.CharField(max_length=50, db_index=True, verbose_name='Вид животного')

    def __str__(self):
        return self.animal_name

    class Meta:
        verbose_name = 'Животное'
        verbose_name_plural = 'Животные'
        ordering = ['animal_name']

class Search(models.Model):
    looking_for = models.CharField(max_length=50, db_index=True, verbose_name='Наименование категории')

    def __str__(self):
        return self.looking_for

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['looking_for']