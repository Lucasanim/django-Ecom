from django.db import models
from django.shortcuts import reverse
# Create your models here.

CATEGORY_CHOICES = (
    ('S','Shirt'),
    ('SW','Sport wear'),
    ('OW','Outwear')
)

LABEL_CHOICES = (
    ('P','primary'),
    ('D','danger'),
    ('S','secondary')
)

class Device(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class User(models.Model):
    device = models.CharField(max_length=100)
    first_name= models.CharField(max_length=150, blank=True, null=True)
    last_name= models.CharField(max_length=150, blank=True, null=True)
    email= models.EmailField(max_length=250, null=True, blank=True)
    phone= models.IntegerField(blank=True, null=True)
    address= models.CharField(max_length=250, blank=True, null=True)
    localidad= models.CharField(max_length=150, blank=True, null=True)
    zip_code= models.IntegerField(blank=True, null=True)

    def __str__(self):
        if self.first_name:
            return f'{self.first_name} {self.last_name}'
        else:
            return self.device

class Item(models.Model):
    title = models.CharField(max_length=150)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField()

    def __str__(self):
        return self.title

    def get_abslute_url(self):
        return reverse('shop:detail', kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse('shop:add_to_cart', kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse('shop:remove_from_cart', kwargs={
            'slug': self.slug
        })

class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}, {self.item}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        else:
            return self.get_total_item_price()

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    items = models.ManyToManyField(OrderItem)

    start_date = models.DateTimeField(auto_now_add=True)

    ordered_date = models.DateTimeField()

    ordered = models.BooleanField(default=False)

    payment = models.ForeignKey('Payments', on_delete=models.SET_NULL, blank=True, null=True)

    cupon = models.ForeignKey('Cupon', on_delete=models.SET_NULL, blank=True, null=True)

    received = models.BooleanField(default=False)

    def __str__(self):
        if self.user.first_name:
            return self.user.first_name
        else:
            return self.user.device

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()

        if self.cupon:
            total -= self.cupon.amount
        return total

class Payments(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.user.first_name:
            return self.user.first_name
        else:
            return self.user.device

class Cupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code