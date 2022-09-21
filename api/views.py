from django.shortcuts import render, redirect
import stripe
from .models import Item
from django.views.decorators.csrf import csrf_protect
# Create your views here.

def index(request):
    """HomePAGE"""

    stripe.api_key = \
        "sk_test_51Lk50oFwCkJDH6LoQm44bpa3Bq92QKlMUN4pCSZYrIUlDbUS8mUB27wMPS05nExMEMJh4TwQYG1vCetmTlG0kDey00c0i11xC"
    context = {'url': 'http://localhost.com'}
    return render(request, 'stripeApi_template/index.html', context)

def item(request, item_id):
    item = Item.objects.get(id=item_id)
    context = {'item': item}


    return render(request, 'stripeApi_template/item.html', context)

def buy(request, buy_id):
    stripe.api_key = "sk_test_51Lk50oFwCkJDH6LoQm44bpa3Bq92QKlMUN4pCSZYrIUlDbUS8mUB27wMPS05nExMEMJh4TwQYG1vCetmTlG0kDey00c0i11xCE"

    item = Item.objects.get(id=buy_id)
    session = stripe.checkout.Session.create(
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': item.name,
                },
                'unit_amount': int(item.price * 100),
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://127.0.0.1:8000/success.html',
        cancel_url='http://127.0.0.1:8000/cancelled.html',
    )

    return redirect(session.url, code=303)

def success(request):
    return render(request, 'stripeApi_template/succsess.html')

def cancelled(request):
    return render(request, 'stripeApi_template/cancelled.html')