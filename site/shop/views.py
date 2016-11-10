from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product
from cart.forms import CartAddProductForm
from cart.cart import Cart


def product_list(request, category_slug=None):
    products = Product.objects.filter(available=True).order_by('-updated')
    title = 'Shop'
    category_list = Category.objects.all()

    if category_slug:
        products = products.filter(category__slug=category_slug)
        title = Category.objects.get(slug=category_slug)

    def products_count(count=0):
        for product in products:
            if product:
                count += 1
        return count

    return render(request, 'shop/shop_index.html',
                  {'products': products, 'category_list': category_list,
                   'title': title, 'count': products_count()})


def product_detail(request, category_slug, id, slug):
    category_list = Category.objects.all()
    category = Category.objects.get(slug=category_slug)
    product = get_object_or_404(Product, id=id, slug=slug)
    start_price = product.price * 70 / 100
    end_price = product.price * 130 / 100
    cart_product_form = CartAddProductForm(
        request.POST if request.method == 'POST' else None, product=product)
    similar_products = Product.objects.filter(
        category=category, price__range=(start_price, end_price)).exclude(id=id)[:4]
    title = product.name
    button = '<<< Back to %s' % category.name

    if request.method == 'POST':
        if cart_product_form.is_valid():
            cart = Cart(request)
            cart.add(product=product, quantity=cart_product_form.cleaned_data[
                     'quantity'], update_quantity=False)
            return redirect('cart:cart_detail')

    return render(request, 'shop/product_detail.html', {
        'product': product,
        'title': title,
        'similar_products': similar_products,
        'category_list': category_list,
        'cart_product_form': cart_product_form,
        'button': button,
    })
