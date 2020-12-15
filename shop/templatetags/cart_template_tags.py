from django import template
from shop.models import Order, User

register = template.Library()

@register.filter
def cart_item_count(request):
    device = request.COOKIES['device']
    user = None
    try:
        user = User.objects.get(device=device)
    except:
        return 0
    if user:
            
        qs = Order.objects.filter(user=user, ordered=False)
        if qs.exists():
            return qs[0].items.count()
    else:
        return 0
