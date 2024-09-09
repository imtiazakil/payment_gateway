from django.urls import reverse
import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .models import Payment
from django.http import JsonResponse
import uuid


def home(request):
    return render(request,'payment.html')




def create_payment(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        amount = request.POST.get('amount')

        if not all([name, email, amount]):
            messages.error(request, "All fields are required.")
            return redirect('payment-form')

        tran_id = str(uuid.uuid4())

        api_data = {
            "store_id": "aamarpaytest",
            "signature_key": "dbb74894e82415a2f7ff0ec3a97e4183",
            "cus_name": name,
            "cus_email": email,
            "cus_phone": "01870762472",
            "amount": amount,
            "currency": "BDT",
            "tran_id": tran_id,
            "desc": "test transaction",
            "success_url": "http://127.0.0.1:8000/payment/payment-callback/",
            "fail_url": "http://127.0.0.1:8000/payment/payments/callback",
            "cancel_url": "http://127.0.0.1:8000/payment/payments/callback",
            "type": "json"
        }

        api_url = 'https://sandbox.aamarpay.com/jsonpost.php'
        try:
            response = requests.post(api_url, json=api_data, headers={'Content-Type': 'application/json'})
            response_data = response.json()
            
            if response_data.get('result') == 'true':
                payment_url = response_data.get('payment_url')

                # Save form data and API response
                payment = Payment(
                    name=name,
                    email=email,
                    amount=amount,
                    tran_id=tran_id,
                    response_data=response_data,
                    status=0  # Initially unpaid
                )
                payment.save()

                # Redirect to payment URL
                return redirect(payment_url)
            else:
                messages.error(request, "Payment initiation failed. Please try again.")
                return redirect('payment-form')

        except Exception as e:
            messages.error(request, f"Error processing payment: {e}")
            return redirect('payment-form')

    return render(request, 'payment.html')


@csrf_exempt
def payment_callback(request):
    if request.method == 'POST':
        transaction_id = request.POST.get('mer_txnid')
        payment_status = request.POST.get('pay_status')
        # Process the data
        try:
            payment = Payment.objects.get(tran_id=transaction_id)
            payment.status = 1 if payment_status == 'Successful' else 0
            payment.save()

            # Set the status flag or context for the redirect
            request.session['payment_status'] = 'Successful' if payment_status == 'Successful' else 'Failed'

        except Payment.DoesNotExist:
            return JsonResponse({'status': 'error'}, status=404)

        # Redirect to a page that will show the message
        return redirect(reverse('payment-status'))

    return JsonResponse({'status': 'error'}, status=400)

def payment_status(request):
    status = request.session.pop('payment_status', 'unknown')  # Retrieve and remove the flag from session
    return render(request, 'payment_status.html', {'status': status})