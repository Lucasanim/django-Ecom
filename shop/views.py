from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, View, ListView, DetailView
from .models import Item, Order, OrderItem, Device, User
from django.utils import timezone
from django.shortcuts import redirect
# Create your views here.

class home(ListView):
    model=Item
    template_name='shop/home-page.html'
    # def get(self, request, *args, **kwargs):
    #     device = request.COOKIES['device']
    #     print('device: ', device)
    #     return render(request, 'shop/index.html')
    
class Shop (ListView):
    model=Item
    template_name='shop/home-page.html'

class ProductDetail(DetailView):
    model=Item
    template_name='shop/product-page.html'


def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug = slug)


    device = request.COOKIES['device']
    print('devide: ', device)

    user = None
    try:
        user = User.objects.get(device=device)
    except:
        pass

    if (user == None):
        user = User.objects.create(device=device)
    

    complete_user = {'device':user.device}

    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user = user,
        ordered=False,
        
    )

    order_qs = Order.objects.filter(user=user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        #check if the order item is in the order
        if order.items.filter(item__slug = item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, 'One more item added to your cart.')
            return redirect('shop:detail',slug=slug)
        else:
            order.items.add(order_item)  
            messages.info(request, 'item added to your cart.')
            return redirect('shop:detail',slug=slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user = user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, 'item added to your cart.')

        return redirect('shop:detail',slug=slug)


def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug = slug)

    device = request.COOKIES['device']
    print('devide: ', device)

    user = None
    try:
        user = User.objects.get(device=device)
    except:
        pass

    order_qs = Order.objects.filter(user=user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        #check if the order item is in the order
        if order.items.filter(item__slug = item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user = user,
                ordered=False,
                
            )[0]
        
            order.items.remove(order_item) 

            messages.info(request, 'item removed from your cart.')

            return redirect('shop:detail', slug=slug)

        else:
            #add a message sayin the user doesnt have an order
            messages.info(request, 'item is not in your cart.')
            return redirect('shop:detail', slug=slug)    
    else:
        #add a message sayin the user doesnt have an order
        messages.info(request, 'You have not an active order.')
        return redirect('shop:detail', slug=slug)


