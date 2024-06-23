from django.shortcuts import render, get_object_or_404
from .cart import Cart
from customer.models import MenuItem
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from customer.models import MenuItem, OrderModel, OrderItem

# Create your views here.
def cart_summary(request):
    cart = Cart(request)
    cart_items = cart.get_items()
    quantities = cart.get_quants()
    totals = cart.cart_total()
    #quantity cart
    total_quantity = 0
    for item_id, quantity in quantities.items():
        total_quantity += quantity

    return render(request, "cart_summary.html", {'cart_items': cart_items, 'quantities':quantities, 'totals':totals, 'total_quantity': total_quantity})

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
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        item_id = request.POST.get('item_id')
        cart.delete(item=item_id)  
        response = JsonResponse({'id': item_id})
        return response
    



def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        item_id = request.POST.get('item_id')
        if item_id is not None:
            item_id = int(item_id)
        item_qty = request.POST.get('item_qty')

        cart.update(item=item_id, quantity=item_qty)

        response = JsonResponse({'qty': item_qty})
        return response
    
