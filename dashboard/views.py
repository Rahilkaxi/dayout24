from django.shortcuts import render, redirect
from .forms import CreateProduct
from products.models import Product
# from django.views.generic import ListView
from cart.decorators import superuser_check

from products.filters import ProductFilter


# Create your views here.

@superuser_check
def dashboard(request):
    context = {}
    return render(request, 'dashboard/dist/index.html', context)


def productlist(request):
    product_list = Product.objects.all()
    product_filter = ProductFilter(request.GET, queryset=product_list)
    return render(request, 'dashboard/dist/productlist.html', {'filter': product_filter})


@superuser_check
def createProduct(request):
    form = CreateProduct()
    if request.method == 'POST':
        # print('printing POST:', request.POST)
        form = CreateProduct(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dash:c-p')

    context = {'form': form}
    return render(request, 'dashboard/dist/product.html', context)


def updateProduct(request, pk):
    product = Product.objects.get(id=pk)
    form = CreateProduct(instance=product)

    if request.method == 'POST':
        form = CreateProduct(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('dash:p-l')

    context = {'form': form}
    return render(request, 'dashboard/dist/product.html', context)


def deleteProduct(request, pk):
    product = Product.objects.get(id=pk)
    product.delete()
    return redirect('dash:p-l')
    contex = {}
    return render(request, 'dashboard/dist/productlist.html', contex)
