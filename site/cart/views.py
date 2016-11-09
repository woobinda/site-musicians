from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product, Category
from .cart import Cart
from .forms import CartAddProductForm
from coupons.forms import CouponApplyForm


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST, product=product)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    category_list = Category.objects.all()
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'update': True}, product=item['product'])
    coupon_apply_form = CouponApplyForm()

    return render(request, 'shop/cart_detail.html', {'cart': cart,
                                                     'coupon_apply_form': coupon_apply_form,
                                                     'title': 'Your shoping Cart',
                                                     'category_list': category_list,
                                                     })
