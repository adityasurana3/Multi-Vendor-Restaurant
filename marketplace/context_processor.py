from .models import Cart
import datetime

def get_cart_counter(request):
    cart_count = 0
    if request.user.is_authenticated:
        try:
            cart_items = Cart.objects.filter(user=request.user)
            # print("cart items=>",cart_items)
            if cart_items:
                for cart_item in cart_items:
                    cart_count += cart_item.quantity
            else:
                cart_count=0
        except:
            cart_count = 0
    return dict(cart_count=cart_count)

