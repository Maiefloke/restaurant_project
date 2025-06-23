from django.db import models
from django.contrib.auth.models import User
from django.conf import settings



# Create your models here.

class Dish(models.Model):
    CATEGORY_CHOICES = [
        ('Сети', 'Сети'),
        ('Роли', 'Роли'),
        ('Супи', 'Супи'),
        ('Напої', 'Напої'),
        ('Десерти', 'Десерти'),

    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='dishes/', default='default.jpg')
    is_popular = models.BooleanField(default=False)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Сети')

    def __str__(self):
        return self.name


class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.dish.name} ({self.quantity})"

    def total_price(self):
        return self.quantity * self.dish.price

    def get_total_price(self):
        return self.dish.price * self.quantity


class Order(models.Model):
    PAYMENT_CHOICES = [
        ('cash', 'Готівка при отриманні'),
        ('online', 'Онлайн-оплата'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Замовлення #{self.id} від {self.full_name}"

    def repeat_order(self):
        new_order = Order.objects.create(
            user=self.user,
            full_name=self.full_name,
            phone=self.phone,
            address=self.address,
            payment_method=self.payment_method,
        )
        for item in self.items.all():
            OrderItem.objects.create(
                order=new_order,
                dish=item.dish,
                quantity=item.quantity,
                price=item.price,
            )
        return new_order

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def get_total_price(self):
        return self.quantity * self.price


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} — {self.dish} — {self.rating}"