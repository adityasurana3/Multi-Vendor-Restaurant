from django.contrib import admin
from .models import Vendor

# Register your models here.
class VendorAdmin(admin.ModelAdmin):
    list_display = ('user','vendor_name','is_apporoved','created_at')
    list_display_links = ('user','vendor_name')
    list_editable = ('is_apporoved',)

admin.site.register(Vendor,VendorAdmin)