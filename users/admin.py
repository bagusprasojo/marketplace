from django.contrib import admin
from .models import User, Provinsi, Kabupaten, Kecamatan, Kelurahan, Alamat

class AlamatAdmin(admin.ModelAdmin):
    model = Alamat
    extra = 1
    fields = ('user','nama_alamat', 'provinsi', 'kabupaten', 'kecamatan', 'kelurahan', 'detail_alamat', 'kode_pos', 'is_default')    
    list_display = ('user', 'nama_alamat', 'provinsi', 'kabupaten', 'kecamatan', 'kelurahan', 'detail_alamat', 'kode_pos', 'is_default')
    # readonly_fields = ('provinsi', 'kabupaten', 'kecamatan', 'kelurahan')

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.form.base_fields['provinsi'].queryset = Provinsi.objects.all()
        formset.form.base_fields['kabupaten'].queryset = Kabupaten.objects.none()
        formset.form.base_fields['kecamatan'].queryset = Kecamatan.objects.none()
        formset.form.base_fields['kelurahan'].queryset = Kelurahan.objects.none()

        if obj:
            formset.form.base_fields['kabupaten'].queryset = Kabupaten.objects.filter(provinsi=obj.provinsi)
            formset.form.base_fields['kecamatan'].queryset = Kecamatan.objects.filter(kabupaten__provinsi=obj.provinsi)
            formset.form.base_fields['kelurahan'].queryset = Kelurahan.objects.filter(kecamatan__kabupaten__provinsi=obj.provinsi)

        return formset
    
class KabupatenAdmin(admin.ModelAdmin):
    model = Kabupaten
    extra = 1
    fields = ('name', 'provinsi')
    list_display = ('name', 'provinsi')
    # readonly_fields = ('provinsi',) 

class KecamatanAdmin(admin.ModelAdmin):
    model = Kecamatan
    extra = 1
    fields = ('name', 'kabupaten')
    list_display = ('name', 'kabupaten')

class KelurahanAdmin(admin.ModelAdmin):
    model = Kelurahan
    extra = 1
    fields = ('name', 'kecamatan')
    list_display = ('name', 'kecamatan')

admin.site.register(User)
admin.site.register(Alamat, AlamatAdmin)
admin.site.register(Provinsi)
admin.site.register(Kabupaten, KabupatenAdmin)
admin.site.register(Kecamatan, KecamatanAdmin)
admin.site.register(Kelurahan, KelurahanAdmin)
