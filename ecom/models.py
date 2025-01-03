from django.db import models
from django.contrib.auth.models import User
import uuid
from ckeditor.fields import RichTextField
# Create your models here.


class HeroSection(models.Model):
    title = models.CharField(max_length=500, default="Discover Your Next Favorite Product")
    description = models.TextField(default="Shop our latest collections and exclusive offers")
    button_text = models.CharField(max_length=50, default="Shop Now")
    background_image = models.ImageField(upload_to='hero_images/', blank=True, null=True)

    def __str__(self):
        return self.title
    

class HeroSectionImage(models.Model):
    hero_section = models.ForeignKey(HeroSection, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='hero_images/')




class banner(models.Model):
    banner_msg = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.banner_msg


class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/CustomerProfilePic/',null=True,blank=True, default="-")
    address = models.CharField(max_length=100)
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
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)  # Add image field

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
    name = models.CharField(max_length=500)
    product_image = models.ImageField(upload_to='product_image/', null=True, blank=True, default="-")
    additional_image1 = models.ImageField(upload_to='product_image/other/', null=True, blank=True)
    additional_image2 = models.ImageField(upload_to='product_image/other/', null=True, blank=True)
    additional_image3 = models.ImageField(upload_to='product_image/other/', null=True, blank=True)
    additional_image4 = models.ImageField(upload_to='product_image/other/', null=True, blank=True)
    price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(null=True, blank=True, help_text="Discount Price")
    description = RichTextField()
    short_description = RichTextField(null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', default=1)
    sub_category = models.ForeignKey(Sub_category, on_delete=models.CASCADE, related_name='products', default=1)
    is_digital = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    popular = models.BooleanField(default=False)
    colors = models.ManyToManyField(Color, blank=True, related_name='products')  # Added color options
    free_delivery = models.BooleanField(default=False)
    priority = models.IntegerField(default=1000)
    popular_priority = models.IntegerField(default=1000)
    feautered_priority = models.IntegerField(default=1000)
    exclusive = models.BooleanField(default=False, help_text="Select this product to display exclusively")


    def final_price(self):
        if self.discount:
            return self.price - self.discount
        return self.price

    def __str__(self):
        return self.name
    



class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Order Confirmed', 'Order Confirmed'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )
    PAYMENT_STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
    )
    order_number = models.CharField(max_length=100, unique=True, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    payment_status = models.CharField(max_length=50, choices=PAYMENT_STATUS_CHOICES, default='Pending')
    order_date = models.DateField(auto_now_add=True, null=True)
    email = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=500, null=True)
    mobile = models.CharField(max_length=20, null=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    address_line_1 = models.CharField(max_length=500, null=True)
    address_line_2 = models.CharField(max_length=500, null=True, blank=True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    zip_code = models.CharField(max_length=20, null=True)
    country = models.CharField(max_length=100, null=True)
    notes = models.TextField(null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    payment_method = models.CharField(max_length=50, null=True)
    delivery_fee = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = str(uuid.uuid4()).replace('-', '').upper()[:8]  # Generate unique order number
        super(Order, self).save(*args, **kwargs)
 
    def can_cancel(self):
        # Allow cancellation only if the status is not 'Out for Delivery' or beyond
        return self.status not in ['Out for Delivery', 'Delivered', 'Cancelled']

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    @property
    def total_price(self):
        return self.product.price * self.quantity
    
    


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
    

#For payment intregation



