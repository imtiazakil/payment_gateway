# myapp/urls.py

from django.urls import path
from . import views  # Import the views from the current app


urlpatterns = [
    path('payment-form/', views.home, name='payment-form'),
    path('create-payment/', views.create_payment, name='create-payment'),
    path('payment-callback/', views.payment_callback, name='payment-callback'),
    path('payment-status/', views.payment_status, name='payment-status'),
    
]