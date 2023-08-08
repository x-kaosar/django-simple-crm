from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class Customer(models.Model):
    user         = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name         = models.CharField(max_length=20, null=True)
    email        = models.EmailField(max_length=60, null=True)
    phone        = models.CharField(max_length=11, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self) :
       return self.user.username
    
class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self) :
       return self.name




class Product(models.Model):
    CATEGORY = (
        ('Indoor', 'Indoor'),
        ('Outdoor', 'Outdoor'),
    )

    name         = models.CharField(max_length=20, null=True)
    price        = models.FloatField(max_length=4, null=True)
    category     = models.CharField(max_length=500, null=True, choices=CATEGORY)
    description  = models.CharField(max_length=300, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    tags         = models.ManyToManyField(Tag)

    def __str__(self) :
       return self.name
    


class Order(models.Model):
    STATUS      = (
                ('Delivered','Delivered'),
                ('Pending','Pending'),
                ('Out For Delivery','Out For Delivery'),
            )
    customer     = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product      =  models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    status       = models.CharField(max_length=500, null=True, choices=STATUS)
    note         = models.CharField(max_length=5000, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    


    def __str__(self) :
       return self.product.name


