from django.shortcuts import render, redirect
import json
import datetime
from django.http import JsonResponse
from .models import *
from .utils import cartData, guestOrder
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
# Create your views here.

def store(request):
    data = cartData(request)
    if request.user.is_authenticated:
        messages.success(request, f'Welcome {request.user.customer.name}!')
    cartItems = data['cartItems']
    products=Product.objects.all()
    context={'products':products, 'cartItems':cartItems}
    return render(request, 'store/store.html', context)

def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    context = {'items':items,'order':order,'cartItems':cartItems}
    return render(request, 'store/cart.html', context)

def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    context = {'items':items,'order':order,'cartItems':cartItems}
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    # parse JSON string and convert it into python dictionary
    data = json.loads(request.body)
    productId=data['productId']
    action=data['action']
    customer=request.user.customer
    product=Product.objects.get(id=productId)
    order,created=Order.objects.get_or_create(customer=customer,complete=False)
    orderItem,created=OrderItem.objects.get_or_create(order=order,product=product)
    if action == 'add':
        orderItem.quantity = orderItem.quantity + 1
    elif action == 'remove':
        orderItem.quantity = orderItem.quantity - 1
    # to save the order item
    orderItem.save()
    if orderItem.quantity==0:
        orderItem.delete()
    return JsonResponse('Item was added', safe=False)



@csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data=json.loads(request.body)
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
    else:
        customer,order=guestOrder(request,data)
    total=float(data['form']['total'])
    order.transaction_id=transaction_id
    if total == order.get_cart_total:
        order.complete=True
    order.save()
    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            province=data['shipping']['province'],
            zipcode=data['shipping']['zipcode']
        )
    return JsonResponse('Payment submitted..', safe=False)
