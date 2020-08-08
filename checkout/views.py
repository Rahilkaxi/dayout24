from django.utils.crypto import get_random_string
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from cart.models import Order, Cart
from .models import ShippingForm, ShippingAddress
from django.views.generic.base import TemplateView


def checkout(request):
    # Checkout view
    form = ShippingForm

    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order_items = order_qs[0].orderitems.all()
    order_total = order_qs[0].get_totals()
    context = {"form": form, "order_items": order_items, "order_total": order_total}
    # Getting the saved saved_address
    saved_address = ShippingAddress.objects.filter(user=request.user)
    if saved_address.exists():
        savedAddress = saved_address.first()
        context = {"form": form, "order_items": order_items, "order_total": order_total, "savedAddress": savedAddress}
    if request.method == "POST":
        saved_address = ShippingAddress.objects.filter(user=request.user)
        if saved_address.exists():

            savedAddress = saved_address.first()
            form = ShippingForm(request.POST, instance=savedAddress)
            if form.is_valid():
                shippingaddress = form.save(commit=False)
                shippingaddress.user = request.user
                shippingaddress.save()
        else:
            form = ShippingForm(request.POST)
            if form.is_valid():
                shippingaddress = form.save(commit=False)
                shippingaddress.user = request.user
                shippingaddress.save()

    return render(request, 'checkout/index.html', context)


def payment(request):
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    # start
    order = Order.objects.get(user=request.user, ordered=False)
    orderitems = order.orderitems.all()
    order_total = order_qs[0].get_totals()
    totalCents = float(order_total * 100);
    total = round(totalCents, 2)
    if request.method == 'POST':
        orderId = get_random_string(length=6,
                                    allowed_chars=u'abcdefhijklmnorstuvwxzABCDEFGHIJKLMNOPQRSTUVWXYZ')
        order.ordered = True
        order.orderId = f'{request.user}{orderId}'
        order.save()
        cartItems = Cart.objects.filter(user=request.user)
        for item in cartItems:
            item.purchased = True
            item.save()
            return redirect('checkout:oderView')
    return render(request, 'checkout/payment.html', {"total": total, "items": orderitems, "order": order})


def oderView(request):
    orders = Order.objects.filter(user=request.user, ordered=True)
    if orders.exists():
        return render(request, 'checkout/order.html', {'orders': orders})
    else:
        messages.warning(request, "You do not have an active order")
        return redirect('/')
