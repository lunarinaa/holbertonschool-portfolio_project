from customer.models import MenuItem

class Cart():
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('session_key')
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
        
        self.cart = cart
    
    def add(self, item, quantity):
        item_qty = str(quantity)
        item_id = str(item.id)
        if item_id in self.cart:
            pass
        else:
            # self.cart[item_id] = {'qty': 'cart_quantity' }
            self.cart[item_id] = int(item_qty)
        self.session.modified = True
    
    def __len__(self):
        return len(self.cart)
    
    def get_items(self):
        item_ids = self.cart.keys()
        items = MenuItem.objects.filter(id__in=item_ids)
        return items
    
    def get_quants(self):
        quantities = self.cart
        return quantities