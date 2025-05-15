from django.contrib import admin
from .models import Order, Ekspedisi, EkspedisiDetail


class EkspedisiAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at")
    search_fields = ("name",)   

class EkspedisiDetailAdmin(admin.ModelAdmin):
    list_display = ("ekspedisi", "name", "default_price", "is_active", "created_at")
    search_fields = ("ekspedisi__name", "name") 

admin.site.register(Order)
admin.site.register(Ekspedisi,EkspedisiAdmin)
admin.site.register(EkspedisiDetail,EkspedisiDetailAdmin)
# admin.site.register(Expedition)
