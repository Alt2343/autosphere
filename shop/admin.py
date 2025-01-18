from django.contrib import admin
from .models import Product, Category, Gallery
from django.utils.safestring import mark_safe

# Register your models here.
class GalleryInLine(admin.TabularInline):
    fk_name = 'product'
    model = Gallery
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent', 'get_products_count')
    prepopulated_fields = {'slug':('title',)}

    def get_products_count(self, obj):
        if obj.products:
            return str(len(obj.products.all()))
        else:
            return '0'

    get_products_count.short_description = 'Количество товаров'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'category', 'price', 'created_at', 'quantity', 'size', 'get_photo')
    list_editable = ('price', 'quantity', 'size')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('title', 'price')
    list_display_links = ('pk', 'title',)
    inlines = [GalleryInLine]

    def get_photo(self, odj):
        if odj.images.all():
            return mark_safe(f'<img src="{odj.images.all()[0].image.url}" width="75">')
        else:
            return '-'

    get_photo.short_description = 'Минеатюра'


admin.site.register(Gallery)
