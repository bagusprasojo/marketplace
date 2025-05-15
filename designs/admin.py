from django.contrib import admin
from .models import Design

class DesignAdmin(admin.ModelAdmin):
    list_display = ("name","slug","image","designer")

admin.site.register(Design, DesignAdmin)
# admin.site.register(ProductCategory)
# admin.site.register(ProductColor)
# admin.site.register(ProductColorDetail)
