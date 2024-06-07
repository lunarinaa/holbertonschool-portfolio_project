import json
from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q
from django.core.mail import send_mail
from .models import MenuItem, Category, OrderModel, OrderItem


class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/index.html')


class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/about.html')

class Contact(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/contact.html')


class Order(View):
    def get(self, request, *args, **kwargs):
        # get every item from each category
        desserts = MenuItem.objects.filter(category__name__contains='Dessert')
        drinks = MenuItem.objects.filter(category__name__contains='Drink')
        

        # pass into context
        context = {

            'desserts': desserts,
            'drinks': drinks,
        }

        # render the template
        return render(request, 'customer/order.html', context)

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('country')
        phone = request.POST.get('phone')

        order_items = {
            'items': []
        }

        items = request.POST.getlist('items[]')
        price = 0
        item_ids = []

        order = OrderModel.objects.create(
            price=price,
            name=name,
            email=email,
            street=street,
            city=city,
            state=state,
            phone=phone,
        )

        for item in items:
            menu_item = MenuItem.objects.get(pk=int(item))
            quantity = int(request.POST.get(f'quantity_{item}', 1))

            # Create OrderItem instance for each item with quantity
            order_item = OrderItem.objects.create(
                order=order,
                menu_item=menu_item,
                quantity=quantity
            )

            # Calculate the total price of the order
            order.price += order_item.menu_item.price * order_item.quantity
            order.save()  # Save the updated order with the new price

            # Update item_data to include quantity
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price,
                'quantity': quantity
            }

            order_items['items'].append(item_data)

        for item in order_items['items']:
            price += item['price'] * item['quantity']
            item_ids.append(item['id'])

        order.price = price
        order.save()
        order.items.add(*item_ids)

        body = ('Thank you for your order! Your will be delivered soon!\n'
                f'Your total: {price}\n'
                'Enjoy!')

        send_mail(
            'Thank You For Your Order!',
            body,
            'example@example.com',
            [email],
            fail_silently=False
        )

        context = {
            'items': order_items['items'],
            'price': price
        }

        return redirect('order-confirmation', pk=order.pk)


class OrderConfirmation(View):
    def get(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)

        context = {
            'pk': order.pk,
            'order_items': order.order_items.all(),
            'price': order.price,
        }

        return render(request, 'customer/order_confirmation.html', context)

    def post(self, request, pk, *args, **kwargs):
        data = json.loads(request.body)

        if data['isPaid']:
            order = OrderModel.objects.get(pk=pk)
            order.is_paid = True
            order.save()

        return redirect('payment-confirmation')


class OrderPayConfirmation(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/order_pay_confirmation.html')


class Menu(View):
    def get(self, request, *args, **kwargs):
        menu_items = MenuItem.objects.all()

        context = {
            'menu_items': menu_items
        }

        return render(request, 'customer/menu.html', context)


class MenuSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get("q")

        menu_items = MenuItem.objects.filter(
            Q(name__icontains=query) |
            Q(price__icontains=query) |
            Q(description__icontains=query)
        )

        context = {
            'menu_items': menu_items
        }

        return render(request, 'customer/menu.html', context)
