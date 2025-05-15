from django.contrib import admin
from .models import Color, Product, ProductCategory, ProductColor, ProductColorDetail

from django.utils.html import format_html

class ColorAdmin(admin.ModelAdmin):
    list_display = ("code", "color_preview", "name")
    search_fields = ("code", "name")

    def color_preview(self, obj):
        return format_html(
            '<div style="width: 40px; height: 20px; background-color: {}; border: 1px solid #ccc;"></div>',
            obj.code
        )
    color_preview.short_description = "Preview"


class ProductAdmin(admin.ModelAdmin):
    list_display = ("sku","name","category")

class ProductColorAdmin(admin.ModelAdmin):
    list_display = ("product","color","image","is_default")

class ProductColorDetailAdmin(admin.ModelAdmin):
    list_display = ("productcolor","size","price")

admin.site.register(Color, ColorAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductCategory)
admin.site.register(ProductColor, ProductColorAdmin)
admin.site.register(ProductColorDetail, ProductColorDetailAdmin)
