from .cart import Cart

def cart(request):
    return{'cart': Cart(request)}

def cart_quantity(request):
    cart = Cart(request)
    quantities = cart.get_quants()
    total_quantity = 0
    for item_id, quantity in quantities.items():
        total_quantity += quantity

    return {
        'total_quantity': total_quantity
    }