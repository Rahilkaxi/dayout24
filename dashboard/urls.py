from django.urls import path
from . import views

app_name = 'dash'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('cp/', views.createProduct, name='c-p'),  # for create product
    path('pl/', views.productlist, name='p-l'),  # for create product

    path('up/<str:pk>/', views.updateProduct, name='u-p'),  # for update product
    path('dp/<str:pk>/', views.deleteProduct, name='d-p'),  # for delete product

]
