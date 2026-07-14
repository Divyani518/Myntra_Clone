from django.contrib import admin
from .models import Category, Brand, Product, ProductImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "gender", "is_active", "sort_order")
    list_filter = ("gender", "is_active")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name",)
    prepopulated_fields = {"slug": ("name",)}


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "brand", "gender", "price", "mrp", "stock", "is_featured")
    list_filter = ("gender", "category", "brand", "is_featured")
    search_fields = ("name", "brand__name", "category__name")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductImageInline]
