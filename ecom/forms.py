from django import forms
from django.contrib.auth.models import User
from . import models


class CustomerUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
        
class CustomerForm(forms.ModelForm):
    class Meta:
        model=models.Customer
        fields=['address','mobile','profile_pic']

class ProductForm(forms.ModelForm):
    class Meta:
        model=models.Product
        fields=['name','price','description','product_image', 'category']

#address of shipment
class AddressForm(forms.Form):
    first_name = forms.CharField(max_length=100, label="First Name")
    last_name = forms.CharField(max_length=100, label="Last Name")
    email = forms.EmailField(label="Email")
    mobile = forms.CharField(max_length=15, label="Mobile")
    address_line_1 = forms.CharField(max_length=500, label="Address Line 1")
    address_line_2 = forms.CharField(max_length=500, required=False, label="Address Line 2")
    city = forms.CharField(max_length=100, label="City")
    state = forms.CharField(max_length=100, label="State/Province")
    zip_code = forms.CharField(max_length=20, label="ZIP/Postal Code")
    country = forms.CharField(max_length=100, label="Country")
    notes = forms.CharField(
        max_length=500, required=False, widget=forms.Textarea, label="Order Notes"
    )
class FeedbackForm(forms.ModelForm):
    class Meta:
        model=models.Feedback
        fields=['name','feedback']

#for updating status of order
class OrderForm(forms.ModelForm):
    class Meta:
        model=models.Orders
        fields=['status']

#for contact us page
class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))

#For copun
class CouponApplyForm(forms.Form):
    code = forms.CharField(label="Coupon")


class CustomerLoginForm(forms.Form):
    username = forms.CharField(max_length=150, label="Username", widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


