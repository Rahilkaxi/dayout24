from django.urls import path
from cart.views import add_to_cart, remove_from_cart, CartView, decreaseCart, addcart, Cart
from .views import home, ProductDetail, Home
from . import views
app_name = 'mainapp'

urlpatterns = [
    # path('', Home.as_view(), name='home'),
    path('', home, name='home'),
    path('p', Home.as_view(), name='home'),
    path('product/<slug>/', ProductDetail.as_view(), name='product'),
    path('cart/', CartView, name='cart-home'),
    path('cart/<id>', add_to_cart, name='cart'),
    path('addcart/<id>', addcart, name='addcart'),
    path('decrease-cart/<id>', decreaseCart, name='decrease-cart'),
    path('remove/<id>', remove_from_cart, name='remove-cart'),
    path('signup/', views.signupPage, name='signup'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    # path('dashboard/', views.dashboard, name='dashboard'),
]
