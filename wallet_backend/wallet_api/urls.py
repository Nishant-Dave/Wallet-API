from django.urls import path
from . import views

urlpatterns = [
    path('transaction/', views.transaction_view, name='transaction_view'),
    path('customer/<int:pk>/', views.customer_detail_view, name='customer_detail_view'),
    path('print-chunk/', views.print_chunk, name='print-chunk'),
]
