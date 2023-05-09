from django.contrib import admin
from .models import Category, Product

# Register your models here.
@admin.register(Category)                                                                           # register page with decorator
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}                                                       # auto changing slug by name

@admin.register(Product)                                                                            # register page with decorator
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'slug', 'price', 'in_stock', 'created', 'updated']
    list_filter = ['in_stock', 'is_active']
    list_editable = ['price', 'in_stock']
    prepopulated_fields = {'slug': ('title',)}                                                      # auto changing slug by title