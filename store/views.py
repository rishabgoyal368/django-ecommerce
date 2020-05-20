from django.shortcuts import render, HttpResponse
from .models import *
from django.http import JsonResponse
import json
import datetime
# Create your views here.


def cart_total(request):
    if request.user.is_authenticated:
        customer = request.user.customer  # get user
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        # return HttpResponse(items)
        cartItem = order.get_cart_items
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItem = order['get_cart_items']
        # for i in cart:
        #     cartItem += cart[i]['quantity']
    return cartItem


def store(request):
    cartItem = cart_total(request)
    products = Product.objects.all()
    context = {'products': products, 'cartItem': cartItem}
    return render(request, 'store/store.html', context)


def cart(request):
    cartItem = cart_total(request)
    if request.user.is_authenticated:
        customer = request.user.customer  # get user
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        # return HttpResponse(items)
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']
        for i in cart:
            cartItem += cart[i]['quantity']
            product = Product.objects.get(id=i)
            total = (product.price + cart[i]['quantity'])
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']
            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price':product.price,
                    'imageURL':product.imageURL,
                },
                'quantity': cart[i]['quantity'],
                'get_total': total,
            }
            items.append(item)

    context = {'items': items, 'order': order, 'cartItem': cartItem}
    return render(request, 'store/cart.html', context)


def checkout(request):
    cartItem = cart_total(request)
    if request.user.is_authenticated:
        customer = request.user.customer  # get user
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        # return HttpResponse(items)
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    context = {'items': items, 'order': order, 'cartItem': cartItem}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('item was added', safe=False)


def processOrder(request):
    trasaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        total = float(data['form']['total'])
        order.trasaction_id = trasaction_id

        if total == order.get_cart_total:
            order.complete = True

        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )

    else:
        print('user not logged in')
    return JsonResponse('Payment Complete', safe=False)
