from .models import CartItem

def cart_item_count(request):
    if request.user.is_authenticated:
        count = CartItem.objects.filter(user=request.user, is_ordered=False).count()
    else:
        count = 0
    return {'cart_count': count}
