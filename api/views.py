from django.shortcuts import render, redirect
import stripe
from .models import Item, Order
import environ
from stripePay.settings import HOME_URL

env = environ.Env()
environ.Env.read_env('.env')
# Create your views here.


def index(request):
    """HomePAGE"""

    context = {'url': HOME_URL}
    return render(request, 'stripeApi_template/index.html', context)


def item(request, item_id):
    item = Item.objects.get(id=item_id)
    context = {'item': item}

    return render(request, 'stripeApi_template/item.html', context)


def buy(request, buy_id):
    stripe.api_key = env("TOKEN")

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
        success_url=HOME_URL + 'success.html',
        cancel_url=HOME_URL + 'cancelled.html',
    )

    return redirect(session.url, code=303)


def success(request):
    # delete order of the item
    completed_order = Order.objects.all().delete()
    return render(request, 'stripeApi_template/success.html')


def cancelled(request):
    return render(request, 'stripeApi_template/cancelled.html')

def shopping_cart(request):
    items = Item.objects.all()
    if not Order.objects.all():
        for item in items:
            sample_item = Order(item=item)
            sample_item.save()
    sample_items = Order.objects.all()
    context = {'items': sample_items}

    return render(request, 'stripeApi_template/shopping_cart.html', context)


def edit_sh_cart(request, item_id):

    if request.method == 'POST':
        item = Item.objects.get(id=item_id)

        if 'add' in request.POST:
            new_item = Order.objects.get(item=item)
            Order.objects.filter(item=item).update(quantity=new_item.quantity+ 1)
            new_item.refresh_from_db()
        elif 'remove' in request.POST:
            try:
                new_item = Order.objects.get(item=item)
                Order.objects.filter(item=item).update(quantity=new_item.quantity- 1)
            except:
                new_item = Order.objects.get(item=item)
                Order.objects.filter(item=item).update(quantity=0)
                new_item.refresh_from_db()
                # try delete from order

    items = Order.objects.all()

    context = {'items': items}

    return render(request, 'stripeApi_template/shopping_cart.html', context)


def order(request):

    stripe.api_key = env("TOKEN")

    items = Order.objects.all()

    line_items =[]
    for item in items:
        if item.quantity != 0:
            line_item={
            'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item.item.name,
                    },
                    'unit_amount': int(item.item.price * 100),
                },
                'quantity': item.quantity,
            }
            line_items.append(line_item)

    session = stripe.checkout.Session.create(
        line_items=line_items,
        mode='payment',
        success_url=HOME_URL+'success.html',
        cancel_url=HOME_URL+'cancelled.html',
    )

    return redirect(session.url, code=303)
