from cart.models import CartItem, CartUser
from market import settings
from products.models import Products
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from products.models import Products
from .forms import CartAddProductForm

# Create your views here.

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    
    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }
        if override_quantity:  ## перезаписать количество (товара)
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity']+= quantity
        self.save()


    def save(self):
        self.session.modified = True


    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()


    def __iter__(self):
        product_ids = self.cart.keys()
        products = Products.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

        
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()



@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Products, id=product_id)
    form = CartAddProductForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data  ## Усли форма валидна, то создается словарик
        cart.add(product=product,
                 quantity=cd['quantity'],
                 override_quantity=cd['override'])
    
    else:
        cart.add(product=product,
                 quantity=1,
                 override_quantity=False)
        
    return redirect('cart:cart-detail')  ## Указать место в которое будет переводить после добавления в карзину


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Products, id=product_id)
    cart.remove(product)

    return redirect('cart:cart-detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'override': True})
    return render(request, 'cart/cart-detail.html', {'cart':cart})


class ProductCartUser:
    def __init__(self, request):
        self.cart = {}
        self.user = request.user

        user_cart, created = CartUser.objects.get_or_create(user=self.user)
        products_in_cart = CartItem.objects.filter(cart=user_cart)

        for item in products_in_cart:  ## Проходим по элементам в корзинеи смотрим что там
            self.cart[str(item.product.id)] = {'quantity': str(item.quantity), 'price': str(item.product.price)}


    def add_cart(self, product, quantity=1, override_quantity=False):
        product_id = str(product_id)
        product = Products.objects.get(pk=product_id)

        if product_id not in self.cart:
            self.cart[product_id]={'quantity': str(quantity), 'price': str(product.price)}
            
        else:
            if not override_quantity:
                current_quantity = int(self.cart[product_id]['quantity'])
                self.cart[product_id]['quantity'] = str(current_quantity+quantity)
            else:
                self.cart[product_id]['quantity'] = quantity

        self.save()

    def save(self):
        for id in self.cart:
            product = Products.objects.get(pk=int(id))
            user_cart = CartUser.objects.get(user=self.user)

            if CartItem.objects.filter(cart=user_cart, product=product).exists():  ## exist - существует
                item = CartItem.objects.get(product=product)
                item.quantity = self.cart[id]['quantity']
                item.save()
            else:
                CartItem.objects.create(cart=user_cart, product=product, quantity=self.cart[id]['quantity'])


    # def __len__(self):
    #     return sum(int(item['quantity'])) for 