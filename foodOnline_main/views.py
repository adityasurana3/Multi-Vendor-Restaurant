from django.shortcuts import render
from vendor.models import Vendor

def home(request):
    vendors = Vendor.objects.filter(is_apporoved = True,user__is_active = True)[:8]
    # print(vendors)
    context = {
        'vendors':vendors
    }
    return render(request,'home.html',context)