from django.urls import path 
from django.contrib import admin
from . views import checkout, payment, oderView, CancelOrder

app_name = "checkout"

urlpatterns = [
	path('checkout/', checkout, name="index"),
	path('payment/', payment, name="payment"),
	# path('charge/', charge, name="charge"),
	path('my-orders/', oderView, name="oderView"),
    path('CO/<str:pk>/', CancelOrder, name='cancel-order'),  # for delete product
]