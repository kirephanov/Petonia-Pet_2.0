from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *

class MarkerAdmin(admin.ModelAdmin):
    list_display = ('id', 'search', 'animal', 'name', 'telephone', 'street', 'city', 'region', 'country', 'created_at', 'get_photo')
    list_display_links = ('id', 'search', 'animal', 'name', 'telephone', 'street', 'city', 'region', 'country')
    search_fields = ('name', 'street', 'city', 'region', 'country')
    list_filter = ('search', 'animal', 'region')
    fields = ('search', 'animal', 'name', 'telephone', 'street', 'city', 'region', 'country', 'comment', 'photo', 'get_photo', 'created_at')
    readonly_fields = ('get_photo', 'created_at')

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="75">')

    get_photo.short_description = 'Фото'

class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'reg_name')
    list_display_links = ('id', 'reg_name')
    search_fields = ('reg_name',)

class AnimalAdmin(admin.ModelAdmin):
    list_display = ('id', 'animal_name')
    list_display_links = ('id', 'animal_name')
    search_fields = ('animal_name',)

class SearchAdmin(admin.ModelAdmin):
    list_display = ('id', 'looking_for')
    list_display_links = ('id', 'looking_for')

admin.site.register(Marker, MarkerAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Animal, AnimalAdmin)
admin.site.register(Search, SearchAdmin)

admin.site.site_title = 'Управление Petonia - Поиск питомцев'
admin.site.site_header = 'Управление Petonia - Поиск питомцев'

