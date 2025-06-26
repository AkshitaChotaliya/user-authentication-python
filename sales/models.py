from django.db import models

# Create your models here.
class Customer(models.Model):
    customer_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    address = models.TextField()
    demographics = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.customer_id})"
    
class Product(models.Model):
    product_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.product_id})"
    
    
class Order(models.Model):
    order_id = models.CharField(max_length=100, unique=True)
    customer = models.ForeignKey('sales.Customer', on_delete=models.CASCADE, related_name='orders')
    date_of_sale = models.DateField()
    region = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"Order {self.order_id} - {self.customer.name}"

class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='order_items')
    quantity_sold = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity_sold} x {self.product.name} (Order {self.order.order_id})"
