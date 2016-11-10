# -*- coding: utf-8 -*-
from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from .tasks import order_created
from cart.cart import Cart
from shop.models import Category
from django.core.exceptions import ValidationError


def order_create(request):
    cart = Cart(request)
    categories = Category.objects.all()
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()

            for item in cart:
                order.add(product=item['product'],
                          price=item['price'],
                          quantity=item['quantity'])

            cart.clear()
            order_created(order.id)

            return render(request, 'shop/order_created.html', {'order': order,
                                                               'title': 'Successfully Created'})
    else:
        form = OrderCreateForm()

    return render(request, 'shop/order.html', {'cart': cart,
                                               'form': form,
                                               'title': 'Checkout',
                                               'categories': categories,
                                               })
