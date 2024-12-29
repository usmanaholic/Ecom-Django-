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
    first_name = forms.CharField(max_length=100, label="First Name", widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, label="Last Name", widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'class': 'form-control'}))
    mobile = forms.CharField(max_length=15, label="Mobile", widget=forms.TextInput(attrs={'class': 'form-control'}))
    address_line_1 = forms.CharField(max_length=500, label="Address Line 1", widget=forms.TextInput(attrs={'class': 'form-control'}))
    address_line_2 = forms.CharField(max_length=500, required=False, label="Address Line 2", widget=forms.TextInput(attrs={'class': 'form-control'}))
    city = forms.CharField(max_length=100, label="City", widget=forms.TextInput(attrs={'class': 'form-control'}))
    state = forms.CharField(max_length=100, label="State/Province", widget=forms.TextInput(attrs={'class': 'form-control'}))
    zip_code = forms.CharField(max_length=20, label="ZIP/Postal Code", widget=forms.TextInput(attrs={'class': 'form-control'}))
    country = forms.CharField(max_length=100, label="Country", widget=forms.TextInput(attrs={'class': 'form-control'}))
    notes = forms.CharField(max_length=500, required=False, widget=forms.Textarea(attrs={'class': 'form-control'}), label="Order Notes")
    PAYMENT_CHOICES = [
        ('cod', 'Cash on Delivery'),
        ('online', 'Online Payment'),
    ]
    payment_method = forms.ChoiceField(choices=PAYMENT_CHOICES, widget=forms.RadioSelect)
class FeedbackForm(forms.ModelForm):
    class Meta:
        model=models.Feedback
        fields=['name','feedback']

#for updating status of order
class OrderForm(forms.ModelForm):
    class Meta:
        model=models.Order
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


