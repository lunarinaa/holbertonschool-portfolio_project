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

    def cart_total(self):
        item_ids = self.cart.keys()
        items = MenuItem.objects.filter(id__in=item_ids)
        quantities = self.cart
        total = 0
        for key, value in quantities.items():
            key = int(key)
            for i in items:
                if i.id == key:
                   total = total + (i.price * value)
        return total

    
    def __len__(self):
        return len(self.cart)
    
    def get_items(self):
        item_ids = self.cart.keys()
        items = MenuItem.objects.filter(id__in=item_ids)
        return items
    
    def get_quants(self):
        quantities = self.cart
        return quantities
    
    def update(self, item, quantity):
        item_id = str(item)
        item_qty = int(quantity)

        ourcart = self.cart
        ourcart[item_id] = item_qty

        self.session.modified = True
        return self.cart
    
    def delete(self, item):
        item_id = str(item)
        if item_id in self.cart:
            del self.cart[item_id]

        self.session.modified = True
        return self.cart
    
    def clear(self):
        if 'session_key' in self.session:
            del self.session['session_key']
            self.session.modified = True
        