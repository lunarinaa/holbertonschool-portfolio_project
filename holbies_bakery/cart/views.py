from django.shortcuts import render, get_object_or_404
from .cart import Cart
from customer.models import MenuItem
from django.http import JsonResponse

# Create your views here.
def cart_summary(request):
    cart = Cart(request)
    cart_items = cart.get_items()
    return render(request, "cart_summary.html", {'cart_items': cart_items})

def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        item_id = int(request.POST.get('item_id'))
        item = get_object_or_404(MenuItem, id=item_id)
        item_qty = int(request.POST.get('item_qty'))

        #save to a session
        cart.add(item=item, quantity=item_qty)

        cart_quantity = cart.__len__()

        # response = JsonResponse({'MenuItem: ':item.name})

        response = JsonResponse({'qty: ':cart_quantity})
        return response
    



def cart_delete(request):
    pass
def cart_update(request):
    pass