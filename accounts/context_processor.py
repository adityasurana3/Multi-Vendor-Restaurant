from vendor.models import Vendor
from django.conf import settings

def get_vendor(requset):
    try:
        vendor = Vendor.objects.get(user = requset.user)
    except:
        vendor = None
    return dict(vendor=vendor)

def get_google_api(request):
    return {'GOOGLE_API_KEY':settings.GOOGLE_API_KEY}