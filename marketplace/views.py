from django.shortcuts import render, get_object_or_404
from vendor.models import Vendor
from menu.models import Category,FoodItem
from django.db.models import Prefetch
from django.http import JsonResponse
from .models import Cart
from .context_processor import get_cart_counter

# Create your views here.

def marketplace(request):
    vendors = Vendor.objects.filter(is_apporoved = True,user__is_active = True)
    vendor_count = vendors.count()
    context ={
        'vendors':vendors,
        'vendor_count':vendor_count,
    }
    return render(request,'marketplace/listings.html',context)

def vendor_detail(request,vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
    # prefetch_related will look the data in reverse manner
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditems',
            queryset=FoodItem.objects.filter(is_available = True)
        )
    )
    
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user = request.user)
    else:
        cart_items = None
    
    context = {
        'vendor':vendor,
        'categories':categories,
        'cart_items':cart_items,
    }
    return render(request,'marketplace/vendor_detail.html',context)

def add_to_cart(request,food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                try:
                    chkCart = Cart.objects.get(user = request.user,fooditem=fooditem)
                    chkCart.quantity += 1
                    chkCart.save()
                    # Response go to Frontend
                    return JsonResponse({'status':'success','message':'Increased the food quantity','cart_counter':get_cart_counter(request),'qty': chkCart.quantity})
                except:
                    chkCart = Cart.objects.create(user = request.user,fooditem=fooditem,quantity=1)
                    # Response go to Frontend
                    return JsonResponse({'status':'Failed','message':'Food added to Cart','cart_counter':get_cart_counter(request),'qty': chkCart.quantity})
            except:
                return JsonResponse({'status':'Failed','message':'Food does not exist'})
        else:
            return JsonResponse({'status':'Failed','message':'Invalid request'})

    else:
        return JsonResponse({'status':'login_required','message':'Please login to continue'})
    
def decrease_cart(request,food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                food_item = FoodItem.objects.get(id=food_id)
                try:
                    chkCart = Cart.objects.get(user=request.user,fooditem=food_item)
                    print(chkCart)
                    if chkCart.quantity > 1:
                        chkCart.quantity -= 1
                        chkCart.save()
                        
                    else:
                        chkCart.delete()
                        chkCart.quantity = 0
                    return JsonResponse({'status': 'Success', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity})
                except:
                    return JsonResponse({'status': 'Failed', 'message': 'You do not have this item in your cart!'})
            except:
                return JsonResponse({'status':'Failed','message':'Food does not exist'})
        else:
            return JsonResponse({'status':'Failed','message':'Invalid request'})
    else:
        return JsonResponse({'status':'login_required','message':'Please login to continue'})
    
def cart(request):
    return render(request,'marketplace/cart.html')