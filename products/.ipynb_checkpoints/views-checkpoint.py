from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from products.models import Product

from cart.decorators import login_register_check

from .filters import ProductFilter
from .forms import CreateUserForm

from django.contrib.auth import authenticate, login, logout


class Home(ListView):
    model = Product
    template_name = 'products/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ProductFilter(self.request.GET, queryset=self.get_queryset())
        return context


def home(request):
    product_list = Product.objects.all()
    product_filter = ProductFilter(request.GET, queryset=product_list)
    return render(request, 'products/home.html', {'filter': product_filter})


class ProductDetail(DetailView):
    model = Product


@login_register_check
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('mainapp:home')
        else:
            messages.info(request, 'Username Or Password is incorrect')
            return render(request, 'account/login.html')

    context = {}
    return render(request, 'account/login.html', context)


@login_register_check
def signupPage(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            forms = form.save(commit=False)
            forms.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created ' + user)
            return redirect('mainapp:login')

    context = {'form': form}
    return render(request, 'account/signup.html', context)


def logoutUser(request):
    logout(request)
    return redirect('mainapp:home')
