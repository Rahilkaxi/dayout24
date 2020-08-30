from django.contrib import messages
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from .models import Cart, Order
from products.models import Product
from django.http import HttpResponse
from .decorators import login_register_check


# Add to Cart View

def add_to_cart(request, id):
    item = get_object_or_404(Product, id=id)
    order_item, created = Cart.objects.get_or_create(
        item=item,
        user=request.user,
        purchased=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.orderitems.filter(item__id=item.id).exists():
            order_item.quantity += 1
            order_item.save()
            # messages.info(request, f"{item.name} quantity has updated.")
            return redirect("mainapp:cart-home")
        else:
            order.orderitems.add(order_item)
            messages.info(request, f"{item.name} has added to your cart.")
            return redirect("mainapp:cart-home")
    else:
        order = Order.objects.create(
            user=request.user)
        order.orderitems.add(order_item)
        messages.info(request, f"{item.name} has added to your cart.")
        return redirect("mainapp:cart-home")


def addcart(request, id):
    if request.user.is_authenticated:
        item = get_object_or_404(Product, id=id)
        order_item, created = Cart.objects.get_or_create(
            item=item,
            user=request.user,
            purchased=False
        )
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            # check if the order item is in the order
            if order.orderitems.filter(item__id=item.id).exists():
                if order_item.quantity > 1:
                    order_item.quantity += 1
                    order_item.save()
                messages.info(request, f"{item.name} has already in your cart")
                return redirect("mainapp:home")
            else:
                order.orderitems.add(order_item)
                messages.info(request, f"{item.name} has added to your cart.")
                return redirect("mainapp:home")
        else:
            order = Order.objects.create(
                user=request.user)
            order.orderitems.add(order_item)
            messages.info(request, f"{item.name} has added to your cart.")
            return redirect("mainapp:home")
    else:
        messages.warning(request, "You are not logged in please LogIn or SignUp")
        return redirect("mainapp:home")


# Remove item from cart

def remove_from_cart(request, id):
    if request.user.is_authenticated:
        item = get_object_or_404(Product, id=id)
        cart_qs = Cart.objects.filter(user=request.user, item=item)
        if cart_qs.exists():
            cart = cart_qs[0]
            # Checking the cart quantity
            if cart.quantity > 1:
                cart.quantity -= 1
                cart.save()
            else:
                []
            cart_qs.delete()
        order_qs = Order.objects.filter(
            user=request.user,
            ordered=False
        )
        if order_qs.exists():
            order = order_qs[0]
            # check if the order item is in the order
            if order.orderitems.filter(item__id=item.id).exists():
                order_item = Cart.objects.filter(
                    item=item,
                    user=request.user,
                )[0]
                order.orderitems.remove(order_item)
                messages.warning(request, "This item was removed from your cart+.")
                return redirect("mainapp:home")
            else:
                messages.warning(request, f"{item.name} has removed from your cart.")
                return redirect("mainapp:home")
        else:
            messages.warning(request, "You do not have an active order")
            return redirect("mainapp:home")
    else:
        messages.warning(request, "You are not logged in please LogIn or SignUp")
        return redirect("mainapp:home")


# Cart View

def CartView(request):
    if request.user.is_authenticated:
        user = request.user
        carts = Cart.objects.filter(user=user, purchased=False)
        orders = Order.objects.filter(user=user, ordered=False)

        if carts.exists():
            if orders.exists():
                order = orders[0]
                return render(request, 'cart/home.html', {"carts": carts, 'order': order})
            else:
                messages.warning(request, "You do not have any item in your Cart")
                return redirect("mainapp:home")

        else:
            messages.warning(request, "You do not have any item in your Cart")
            return redirect("mainapp:home")
    else:
        messages.warning(request, "You are not logged in please LogIn or SignUp")
        return redirect("mainapp:home")

        # user = request.user.is_anonymous
        # carts = Cart.objects.filter(user=user, purchased=False)
        # orders = Order.objects.filter(user=user, ordered=False)
        #
        # if carts.exists():
        #     if orders.exists():
        #         order = orders[0]
        #         return render(request, 'cart/home.html', {"carts": carts, 'order': order})
        #     else:
        #         messages.warning(request, "You do not have any item in your Cart")
        #         return redirect("mainapp:home")
        #
        # else:
        #     messages.warning(request, "You do not have any item in your Cart")
        #     return redirect("mainapp:home")


# Decrease the quantity of the cart :

def decreaseCart(request, id):
    item = get_object_or_404(Product, id=id)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.orderitems.filter(item__id=item.id).exists():
            order_item = Cart.objects.filter(
                item=item,
                user=request.user
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.orderitems.remove(order_item)
                order_item.delete()
            # messages.info(request, f"{item.name} quantity has updated.")
            return redirect("mainapp:cart-home")
        else:
            messages.info(request, f"{item.name} quantity has updated1.")
            return redirect("mainapp:cart-home")
    else:
        messages.info(request, "You do not have an active order")
        return redirect("mainapp:cart-home")
