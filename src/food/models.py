from django.db import models
from customers.models import Customer
from suppliers.models import Supplier
import computed_property
# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank = True)
    def __str__(self):
        return self.name


class Meal(models.Model):
    name = models.CharField(max_length=200)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    ingredients = models.ManyToManyField('Ingredient')
    description = models.TextField(blank = True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    image = models.ImageField(upload_to='images/meals', blank=True)
    ceated = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
class Category(models.Model):
    name = models.CharField(max_length=200)
    ceated = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.TextField(blank = True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    def get_total_price(self):
        return self.quantity * self.price



 
class Item(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    def __str__(self):
        return self.meal.name+" "+ str(self.quantity)
    def get_total_item_price(self):
        return self.meal.price * self.quantity
class Order(models.Model):
    STATUS = (
    ('Ordered','Ordered'),
    ('Preparing','Preparing'),
    ('InProgress','InProgress'),
    ('Delivered','Delivered'),
    ('Canceled','Canceled'),
    )
    items = models.ManyToManyField(Item)
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.CASCADE)
    order_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50, choices = STATUS, default='Ordered')
    def __str__(self):
        return "order by "+self.customer.first_name +" "+ self.customer.last_name
    
    def get_total_price(self):
        toata_price = 0
        for item in self.items.all():
            toata_price+= item.get_total_item_price()
        return toata_price



class Invoice(models.Model):
    STATUS = (
    ('Pending','Pending'),
    ('ToAccepting','ToAccepting'),
    ('Accepted','Accepted'),
    ('InProgress','InProgress'),
    ('Delivered','Delivered'),
    ('Canceled','Canceled'),
    )
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    description = models.TextField(blank = True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    status = models.CharField(max_length=50, choices = STATUS, default='Pending')
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    def __str__(self):
        return "invoice: "+self.supplier.first_name +" "+ self.supplier.last_name

    def get_items(self):
        invoiceItems =  self.invoiceitem_set.all() 
        return invoiceItems

    def get_items_price(self):
        toatal_price = 0
        for invoiceItem in self.get_items():
            toatal_price+= invoiceItem.price
        return toatal_price

    def get_items_count(self):
        return self.get_items().count()
        
    def save(self, *args, **kwargs):
        self.price = self.get_items_price()
        super(Invoice, self).save(*args, **kwargs)
    

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    category = models.CharField(max_length=200)
    quantity = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.TextField(blank = True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    def get_total_price(self):
        return self.quantity * self.price