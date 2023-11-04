from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# User Info 
DIVISION_CHOICES = (
    ('','Division Choese'),
    ('Dhaka','Dhaka'),
    ('Khulna','Khulna'),
    ('Rangpur','Rangpur'),
    ('Rajshahi','Rajshahi'),
    ('Barishal','Barishal'),
    ('Chattogram','Chattogram'),
    ('Mymenshing','Mymenshing'),
    ('Sylhet','Sylhet'),
)

class Customar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    division = models.CharField(choices=DIVISION_CHOICES, max_length=150)
    district = models.CharField(max_length=150)
    thana = models.CharField(max_length=75)
    villageORroad = models.CharField(max_length=100)
    zipcode = models.IntegerField()
    
    def __str__(self):
        return str(self.id)
    
    
# Product Category
CATEGORY_CHOICES = (
    ('BF','Baby Fashion'),
    ('GP','Gents Pant'),
    ('BK','Borkha'),
    ('S','Saree'),
    ('L','Lehenga'),
)

class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_rice = models.FloatField()
    discount_price = models.FloatField()
    discription = models.TextField()
    brand = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=4)
    product_img = models.ImageField(upload_to='product_img')
    
    def __str__(self):
        return str(self.id)
    
    
# cart item
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prodcut = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return str(self.id)
    
    @property
    def ammount(self):
        return self.quantity * self.prodcut.discount_price
    
    
# Order Status 
STATUS_CHOICE = (
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On the way','On the way'),
    ('Deliverd','Deliverd'),
    ('Cancel','Cancel'),
)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customar = models.ForeignKey(Customar, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICE, default='pending')
    
    
    @property
    def ammount(self):
        return self.quantity * self.product.discount_price