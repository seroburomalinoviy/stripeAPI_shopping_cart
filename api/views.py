from django.shortcuts import render, redirect
import stripe
from .models import Item, Order, ItemInstance
from stripePay.settings import ALLOWED_HOSTS
from config_reader import load_config


# Create your views here.


def index(request):
    """HomePAGE"""

    context = {'url': ALLOWED_HOSTS[0]}
    return render(request, 'stripeApi_template/index.html', context)


def item(request, item_id):
    item = Item.objects.get(id=item_id)
    context = {'item': item}

    return render(request, 'stripeApi_template/item.html', context)


def buy(request, buy_id):
    config = load_config('config/settings.ini')
    stripe.api_key = config.token

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
        success_url=ALLOWED_HOSTS[0]+'success.html',
        cancel_url=ALLOWED_HOSTS[0]+'cancelled.html',
    )

    return redirect(session.url, code=303)


def success(request):
    completed_order = ItemInstance.object.all().delete()
    completed_order.save()
    return render(request, 'stripeApi_template/success.html')


def cancelled(request):
    return render(request, 'stripeApi_template/cancelled.html')

def shopping_cart(request):
    items = Item.objects.all()
    if not ItemInstance.objects.all():
        # create order
        for item in items:
            sample_item = ItemInstance(item=item)
            sample_item.save()
    sample_items = ItemInstance.objects.all()
    context = {'items': sample_items}

    return render(request, 'stripeApi_template/shopping_cart.html', context)


def edit_sh_cart(request, item_id):

    if request.method == 'POST':
        item = Item.objects.get(id=item_id)
    if 'add' in request.POST:
        new_item = ItemInstance.objects.get(item=item)
        ItemInstance.objects.filter(item=item).update(quantity=new_item.quantity+ 1)
        new_item.refresh_from_db()
    elif 'remove' in request.POST:
        try:
            new_item = ItemInstance.objects.get(item=item)
            ItemInstance.objects.filter(item=item).update(quantity=new_item.quantity- 1)
            new_item.refresh_from_db()
        except:
            new_item = ItemInstance.objects.get(item=item)
            ItemInstance.objects.filter(item=item).update(quantity=0)
            new_item.refresh_from_db()


        # update order

        # order = Order.objects.create()
        # order.item.add(new_item)
        # order.save()

    items = ItemInstance.objects.all()

    context = {'items': items}

    return render(request, 'stripeApi_template/shopping_cart.html', context)

def order(request):
    config = load_config('config/settings.ini')
    stripe.api_key = config.token
    # items = order.objects.first() #? ==ItemInstance.objects.all()
    items = ItemInstance.objects.all()
    line_items =[]
    for item in items:
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
        success_url=ALLOWED_HOSTS[0]+'success.html',
        cancel_url=ALLOWED_HOSTS[0]+'cancelled.html',
    )

    return redirect(session.url, code=303)
