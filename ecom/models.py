from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.
class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/CustomerProfilePic/',null=True,blank=True, default="-")
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name
    

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    featured = models.BooleanField(default=False)  # New field to indicate featured categories

    def __str__(self):
        return self.name
    
class Sub_category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='sub_category', default=1)


    def __str__(self):
        return self.name
    


from django.db import models

class Color(models.Model):
    name = models.CharField(max_length=50, unique=True)


    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    product_image = models.ImageField(upload_to='product_image/', null=True, blank=True, default="-")
    additional_image1 = models.ImageField(upload_to='product_image/other/', null=True, blank=True)
    additional_image2 = models.ImageField(upload_to='product_image/other/', null=True, blank=True)
    additional_image3 = models.ImageField(upload_to='product_image/other/', null=True, blank=True)
    additional_image4 = models.ImageField(upload_to='product_image/other/', null=True, blank=True)
    price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(null=True, blank=True, help_text="Discount percentage")
    description = models.TextField(max_length=1000)
    short_description = models.TextField(max_length=100, null=True)
    stock = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', default=1)
    sub_category = models.ForeignKey(Sub_category, on_delete=models.CASCADE, related_name='products', default=1)
    is_digital = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    popular = models.BooleanField(default=False)
    colors = models.ManyToManyField(Color, blank=True, related_name='products')  # Added color options

    def final_price(self):
        if self.discount:
            return self.price - self.discount
        return self.price

    def __str__(self):
        return self.name



class Orders(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Order Confirmed', 'Order Confirmed'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='order_items', null=True, blank=True)
    email = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=500, null=True)
    mobile = models.CharField(max_length=20, null=True)
    order_date = models.DateField(auto_now_add=True, null=True)
    status = models.CharField(max_length=50, null=True, choices=STATUS)
    
    


class Feedback(models.Model):
    name=models.CharField(max_length=40)
    feedback=models.CharField(max_length=500)
    date= models.DateField(auto_now_add=True,null=True)
    def __str__(self):
        return self.name
    

#For Copun
class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    active = models.BooleanField(default=True)
    users = models.ManyToManyField(User, blank=True)  # Only for specific users if necessary

    def __str__(self):
        return self.code
    

#For Coupons Usage
class CouponUsage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    used_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} used {self.coupon.code}"


class Order(models.Model):
    order_number = models.CharField(max_length=100, unique=True, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    # other fields

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = str(uuid.uuid4()).replace('-', '').upper()[:5]  # Generate unique order number
        super(Order, self).save(*args, **kwargs)




