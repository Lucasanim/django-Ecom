from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, View, ListView, DetailView
from .models import Item, Order, OrderItem, Device, User, Payments, Cupon
from django.utils import timezone
from django.shortcuts import redirect

from .forms import CheckOutForm, CuponForm
# Create your views here.

class home(ListView):
    model=Item
    template_name='shop/home-page.html'
    paginate_by = 10
    # def get(self, request, *args, **kwargs):
    #     device = request.COOKIES['device']
    #     print('device: ', device)
    #     return render(request, 'shop/index.html')

class OrderSummary(View):
    def get(self, request, *args, **kwargs):

        device = request.COOKIES['device']
        print('MyDevide: ', device)

        context=None
        user = None
        try:
            user = User.objects.get(device=device)
            print('user: ', user.device, user.email)
        except:
            pass

        if (user == None):
            user = User.objects.create(device=device)

        try:
            order = Order.objects.get(user=user, ordered=False)

            context={
                'object': order
            }

            return render(request, 'shop/order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(request, 'You have not an active order')
            return redirect('/')

    
class ProductDetail(DetailView):
    model=Item
    template_name='shop/product-page.html'

class CheckOut(View):
    def get(self, request, *args, **kwargs):

        device = request.COOKIES['device']
        order = None
        user = None
        try:
            user = User.objects.get(device=device)
        except:
            pass
        try:
            order = Order.objects.get(user=user, ordered=False)
            
            form = CheckOutForm()
            context = {
                'form':form,
                'order': order,
                'cuponform':CuponForm()
            }

            return render(request, 'shop/checkout-page.html', context)
        
        except ObjectDoesNotExist:
            messages.info(request, 'You have not an active order.')
            return redirect('shop:checkout')

        
    
    def post(self, request, *args, **kwargs):
        form = CheckOutForm(request.POST or None)
        print(request.POST)

        device = request.COOKIES['device']

        user = None
        if form.is_valid():
            print(form.cleaned_data)
            print('valid form')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            phone = form.cleaned_data.get('phone')
            address = form.cleaned_data.get('address')
            localidad = form.cleaned_data.get('localidad')
            zip_code = form.cleaned_data.get('zip_code')
            payment_option = form.cleaned_data.get('payment_option')
            
            try:
                user = User.objects.filter(device=device).update(
                    first_name = first_name,
                    last_name = last_name,
                    email = email,
                    phone = phone,
                    address = address,
                    localidad = localidad,
                    zip_code = zip_code,
                )
            except:
                pass
            
            if payment_option == 'P':
                return redirect('shop:payment', payment_option="Paypal")
            elif payment_option =='MP':
                return redirect('shop:payment', payment_option="Mercado_Pago")
            else:
                messages.warning(request, "Invalid payment option.")
                return redirect('shop:checkout')    
        else:
            messages.warning(request, 'Invalid form.')
            return redirect('shop:checkout')

class Payment(View):
    def get(self, request, *args, **kwargs):
        device = request.COOKIES['device']

        context=None
        user = None
        try:
            user = User.objects.get(device=device)
        except:
            pass

        #order
        order = Order.objects.get(user=user, ordered=False)
        total = order.get_total()
        if user and order.user.first_name:
            return render(request, 'shop/payment.html', {'total':total, 'order':order})
        else:
            messages.error(request, 'JYou have not added you information.')
            return redirect('shop:checkout')

class Payment_aproved(View):
    def get(self, request, *args, **kwargs):
        device = request.COOKIES['device']
        user = None
        amount = None
        try:
            user = User.objects.get(device=device)
        except:
            messages.error(request,'Error validating your payment. Please contact us.')
            return redirect('shop:home')
        if user:
                
            order = Order.objects.get(user=user, ordered=False)
            amount = order.get_total()

            #create the payment
            payment = Payments()
            payment.user = user
            payment.amount = amount
            payment.save()

            #Clear order items
            order_items = order.items.all()
            order_items.update(ordered=True)
            for item in order_items:
                item.save()

            #assign the payment to the order
            order.ordered = True
            order.payment = payment
            order.save()
    
            messages.success(request,'Payment successfully.')

            return redirect('shop:home')

        else:
            messages.error(request,'Error validating your payment. Please contact us.')
            return redirect('shop:home')
        


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
            return redirect('shop:order_summary')
        else:
            order.items.add(order_item)  
            messages.info(request, 'item added to your cart.')
            return redirect('shop:order_summary')
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user = user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, 'item added to your cart.')

        return redirect('shop:order_summary')


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

            return redirect('shop:order_summary')

        else:
            #add a message sayin the user doesnt have an order
            messages.info(request, 'item is not in your cart.')
            return redirect('shop:detail', slug=slug)    
    else:
        #add a message sayin the user doesnt have an order
        messages.info(request, 'You have not an active order.')
        return redirect('shop:detail', slug=slug)


def remove_single_item_from_cart(request, slug):
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

            if order_item.quantity > 1:
                order_item.quantity -= 1    
                order_item.save()
                
            else:
                order.items.remove(order_item)
        
            messages.info(request, 'Item quantity updated.')

            return redirect('shop:order_summary')

        else:
            #add a message sayin the user doesnt have an order
            messages.info(request, 'item is not in your cart.')
            return redirect('shop:detail', slug=slug)    
    else:
        #add a message sayin the user doesnt have an order
        messages.info(request, 'You have not an active order.')
        return redirect('shop:detail', slug=slug)


def get_cupon(request, code):
    try:
        cupon = Cupon.objects.get(code=code)
        return cupon
    except ObjectDoesNotExist:
        messages.info(request, 'This cupon does not exist.')
        return redirect('shop:checkout')


def add_cupon(request):

    if request.method == 'POST':
        form = CuponForm(request.POST or None)

        if form.is_valid():

            device = request.COOKIES['device']
            print('devide: ', device)

            user = None
            try:
                user = User.objects.get(device=device)
            except:
                pass
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(user=user, ordered=False)

                order.cupon = get_cupon(request, code)
                order.save()
                messages.success(request, 'Cupon added correctly!')
                return redirect('shop:checkout')
            
            except ObjectDoesNotExist:
                messages.info(request, 'You have not an active order.')
                return redirect('shop:checkout')
    else:
        return None