from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator

STATE_CHOICE = (
    ('Abbotabad','Abbotabad'),
    ('Ahmadpur East','Ahmadpur East'),
    ('Bahawalnagar','Bahawalnagar'),
    ('Bahawalpur','Bahawalpur'),
    ('Chakwal','Chakwal'),
    ('Chiniot','Chiniot'),
    ('Dera Ismail Khan','Dera Ismail Khan'),
    ('Faisalabad','Faisalabad'),
    ('Gujranwala','Gujranwala'),
    ('Hyderabad','Hyderabad'),
    ('Islamabad','Islamabad'),
    ('Jhelum','Jhelum'),
    ('Karachi','Karachi'),
    ('Khanpur','Khanpur'),
    ('Kohat','Kohat'),
    ('Lahore','Lahore'),
    ('Okara','Okara'),
    ('Peshawar','Peshawar'),
    ('Quetta','Quetta'),
    ('Rawalpindi','Rawalpindi'),
    ('Sargodha','Sargodha'),
    ('Swabi','Swabi'),
    ('Sialkot','Sialkot'),

)
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICE,max_length=50)

    def __str__(self):
        return str(self.id)
CATEGORY_CHOICES = (
    ('M','Mobile'),
    ('L','Laptope'),
    ('TW','Top Wear'),
    ('BW','Bottom Wear'),
)
class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=2)
    product_image = models.ImageField(upload_to="productimg")

    def __str__(self):
        return str(self.id)
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
    
STATUS_CHOICES = (
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel'),

)
class OrderPlaced(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add = True)
    status = models.CharField(choices=STATUS_CHOICES,max_length=50,default='Pending')

