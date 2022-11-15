from vendor.models import Vendor


def get_vendor(requset):
    try:
        vendor = Vendor.objects.get(user = requset.user)
    except:
        vendor = None
    return dict(vendor=vendor)