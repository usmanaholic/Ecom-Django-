from django.shortcuts import render,redirect,reverse,get_object_or_404
from . import forms,models
from django.http import HttpResponseRedirect,HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages
from django.conf import settings
from .models import Category, Product, Coupon, CouponUsage, Orders, Order, Customer, Sub_category
from django.utils import timezone
from .forms import CouponApplyForm
from decimal import Decimal
from django.contrib.auth import authenticate, login
from .forms import CustomerLoginForm
from django.core.paginator import Paginator
from django.contrib.auth.forms import AuthenticationForm
import json



def home_view(request):
    products = models.Product.objects.all()  # Fetch all products
    popular_products = models.Product.objects.filter(popular=True)
    featured_products = models.Product.objects.filter(featured=True)  # Only popular products
    featured_categories = models.Category.objects.filter(featured=True)  # Only featured categories
    categories = models.Category.objects.all()  # All categories
    sub_categories = models.Sub_category.objects.all()

    # Check if product_ids are stored in cookies (for cart count)
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter = product_ids.split('|')
        product_count_in_cart = len(set(counter))  # Count unique items in cart
    else:
        product_count_in_cart = 0

    # Redirect authenticated users to another page after login
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')

    # Pass products, categories, and featured categories to the template
    return render(request, 'ecom/index.html', {
        'products': products,
        'popular_products': popular_products,
        'categories': categories,
        'featured_categories': featured_categories,
        'product_count_in_cart': product_count_in_cart,
        'sub_categories': sub_categories,
        'featured_products': featured_products,
    })

#_______________________________________________
#___________category_______________________________
#____________________________________________________

def category_products_view(request, category_id):
    # Get the category object by its ID or return a 404 if not found
    category = get_object_or_404(Category, id=category_id)
    
    # Filter the products by the selected category
    products = Product.objects.filter(category=category)
    
    # Render a template to show products for this category
    return render(request, 'ecom/category_products.html', {
        'category': category,
        'products': products
    })

#_______________________________________________
#___________sub_category_______________________________
#____________________________________________________
def sub_category_products_view(request, sub_category_id):
    # Get the sub_category object by its ID or return a 404 if not found
    sub_category = get_object_or_404(Sub_category, id=sub_category_id)
    
    # Filter the products by the selected category
    products = Product.objects.filter(sub_category=sub_category)
    
    # Render a template to show products for this category
    return render(request, 'ecom/sub_category_products.html', {
        'sub_category': sub_category,
        'products': products
    })

#_______________________________________________
#___________Navbar view_______________________________
#____________________________________________________


#for showing login button for admin(by usman)
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')


# Customer Signup View
def customer_signup_view(request):
    userForm = forms.CustomerUserForm()
    customerForm = forms.CustomerForm()
    mydict = {'userForm': userForm, 'customerForm': customerForm}

    if request.method == 'POST':
        userForm = forms.CustomerUserForm(request.POST)
        customerForm = forms.CustomerForm(request.POST, request.FILES)
        if userForm.is_valid() and customerForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            customer = customerForm.save(commit=False)
            customer.user = user
            customer.save()
            my_customer_group, created = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group.user_set.add(user)
            return redirect('customerlogin')  # Updated to use `redirect`
    return render(request, 'ecom/customersignup.html', context=mydict)

# Check if user is a customer
def is_customer(user):
    return user.groups.filter(name='CUSTOMER').exists()

# Customer Login View
# Customer Login View
def customer_login_view(request):
    form = forms.CustomerLoginForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('afterlogin')
            else:
                # Add error message if authentication fails
                messages.error(request, "Invalid username or password.")
        else:
            # Add error message if form is invalid
            messages.error(request, "Please check your input and try again.")
    return render(request, 'ecom/customerlogin.html', {"form": form})

# After login view for checking user role
def afterlogin_view(request):
    if is_customer(request.user):
        return redirect('customer-home')
    else:
        return redirect('admin-dashboard')
    

#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    # for cards on dashboard
    customercount=models.Customer.objects.all().count()
    productcount=models.Product.objects.all().count()
    ordercount=models.Orders.objects.all().count()

    # for recent order tables
    orders=models.Orders.objects.all()
    ordered_products=[]
    ordered_bys=[]
    for order in orders:
        ordered_product=models.Product.objects.all().filter(id=order.product.id)
        ordered_by=models.Customer.objects.all().filter(id = order.customer.id)
        ordered_products.append(ordered_product)
        ordered_bys.append(ordered_by)

    mydict={
    'customercount':customercount,
    'productcount':productcount,
    'ordercount':ordercount,
    'data':zip(ordered_products,ordered_bys,orders),
    }
    return render(request,'ecom/admin_dashboard.html',context=mydict)


# admin view customer table
@login_required(login_url='adminlogin')
def view_customer_view(request):
    customers=models.Customer.objects.all()
    return render(request,'ecom/view_customer.html',{'customers':customers})


# admin delete customer
@login_required(login_url='adminlogin')
def delete_customer_view(request,pk):
    customer=models.Customer.objects.get(id=pk)
    user=models.User.objects.get(id=customer.user_id)
    user.delete()
    customer.delete()
    return redirect('view-customer')


@login_required(login_url='adminlogin')
def update_customer_view(request,pk):
    customer=models.Customer.objects.get(id=pk)
    user=models.User.objects.get(id=customer.user_id)
    userForm=forms.CustomerUserForm(instance=user)
    customerForm=forms.CustomerForm(request.FILES,instance=customer)
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST,instance=user)
        customerForm=forms.CustomerForm(request.POST,instance=customer)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customerForm.save()
            return redirect('view-customer')
    return render(request,'ecom/admin_update_customer.html',context=mydict)

# admin view the product
@login_required(login_url='adminlogin')
def admin_products_view(request):
    products=models.Product.objects.all()
    return render(request,'ecom/admin_products.html',{'products':products})


# admin add product by clicking on floating button
@login_required(login_url='adminlogin')
def admin_add_product_view(request):
    productForm=forms.ProductForm()
    if request.method=='POST':
        productForm=forms.ProductForm(request.POST, request.FILES)
        if productForm.is_valid():
            productForm.save()
        return HttpResponseRedirect('admin-products')
    return render(request,'ecom/admin_add_products.html',{'productForm':productForm})


@login_required(login_url='adminlogin')
def delete_product_view(request,pk):
    product=models.Product.objects.get(id=pk)
    product.delete()
    return redirect('admin-products')


@login_required(login_url='adminlogin')
def update_product_view(request,pk):
    product=models.Product.objects.get(id=pk)
    productForm=forms.ProductForm(instance=product)
    if request.method=='POST':
        productForm=forms.ProductForm(request.POST,request.FILES,instance=product)
        if productForm.is_valid():
            productForm.save()
            return redirect('admin-products')
    return render(request,'ecom/admin_update_product.html',{'productForm':productForm})


@login_required(login_url='adminlogin')
def admin_view_booking_view(request):
    orders=models.Orders.objects.all()
    ordered_products=[]
    ordered_bys=[]
    for order in orders:
        ordered_product=models.Product.objects.all().filter(id=order.product.id)
        ordered_by=models.Customer.objects.all().filter(id = order.customer.id)
        ordered_products.append(ordered_product)
        ordered_bys.append(ordered_by)
    return render(request,'ecom/admin_view_booking.html',{'data':zip(ordered_products,ordered_bys,orders)})


@login_required(login_url='adminlogin')
def delete_order_view(request,pk):
    order=models.Orders.objects.get(id=pk)
    order.delete()
    return redirect('admin-view-booking')

# for changing status of order (pending,delivered...)
@login_required(login_url='adminlogin')
def update_order_view(request,pk):
    order=models.Orders.objects.get(id=pk)
    orderForm=forms.OrderForm(instance=order)
    if request.method=='POST':
        orderForm=forms.OrderForm(request.POST,instance=order)
        if orderForm.is_valid():
            orderForm.save()
            return redirect('admin-view-booking')
    return render(request,'ecom/update_order.html',{'orderForm':orderForm})


# admin view the feedback
@login_required(login_url='adminlogin')
def view_feedback_view(request):
    feedbacks=models.Feedback.objects.all().order_by('-id')
    return render(request,'ecom/view_feedback.html',{'feedbacks':feedbacks})



#---------------------------------------------------------------------------------
#------------------------ PUBLIC CUSTOMER RELATED VIEWS START ---------------------
#---------------------------------------------------------------------------------
def search_view(request):
    # whatever user write in search box we get in query
    query = request.GET['query']
    products=models.Product.objects.all().filter(name__icontains=query)
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0

    # word variable will be shown in html when user click on search button
    word="Here You Go! :"

    if request.user.is_authenticated:
        return render(request,'ecom/customer_home.html',{'products':products,'word':word,'product_count_in_cart':product_count_in_cart})
    return render(request,'ecom/index.html',{'products':products,'word':word,'product_count_in_cart':product_count_in_cart})


# any one can add product to cart, no need of signin
from django.utils.http import urlencode


def add_to_cart_view(request, pk):
    products = models.Product.objects.all()
    popular_products = models.Product.objects.filter(featured=True)  # Only popular products
    featured_categories = models.Category.objects.filter(featured=True)  # Only featured categories
    categories = models.Category.objects.all()  # All categories

    # Initialize cart
    if 'cart' in request.COOKIES:
        # Decode cart from cookies
        cart = json.loads(request.COOKIES['cart'])
    else:
        cart = {}

    # Add or update the product in the cart
    if str(pk) in cart:
        cart[str(pk)]['quantity'] += 1  # Increment quantity if product exists
    else:
        product = models.Product.objects.get(id=pk)
        cart[str(pk)] = {'quantity': 1, 'price': product.price}  # Add product with initial quantity

    # Calculate the total number of unique products in the cart
    product_count_in_cart = sum(item['quantity'] for item in cart.values())

    # Prepare the response
    response = render(request, 'ecom/index.html', {
        'products': products,
        'product_count_in_cart': product_count_in_cart,
        'popular_products': popular_products,
        'categories': categories,
        'featured_categories': featured_categories,
    })

    # Save updated cart in cookies
    response.set_cookie('cart', json.dumps(cart))

    # Show success message
    product = models.Product.objects.get(id=pk)
    messages.info(request, f"{product.name} added to cart successfully!")

    return response


# for checkout of cart
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product, Coupon, CouponUsage
import json
from django.utils import timezone

# Cart View
def cart_view(request):
    # For cart counter
    if 'cart' in request.COOKIES:
        cart = json.loads(request.COOKIES['cart'])
        product_count_in_cart = sum(item['quantity'] for item in cart.values())  # Total product count
    else:
        cart = {}
        product_count_in_cart = 0

    # Fetching product details from the database whose ID is present in cookies
    products = []
    total = 0
    delivery_fee = 0  # Initialize delivery fee

    if cart:
        product_ids_in_cart = cart.keys()  # Get all product IDs in cart
        products = Product.objects.filter(id__in=product_ids_in_cart)

        has_physical_product = False  # Flag to check if there's at least one physical product

        # Calculate total price of products in the cart and check for physical products
        for p in products:
            quantity = cart[str(p.id)]['quantity']
            total += p.price * quantity

            # Check if the product is non-digital
            if not p.is_digital:
                has_physical_product = True

        # Add delivery fee only if there's a physical product
        if has_physical_product:
            delivery_fee = 250  # Set your delivery fee value here

    # Coupon application logic
    coupon_discount = 0
    final_total = total + delivery_fee

    if request.method == 'POST' and 'coupon_code' in request.POST:
        coupon_code = request.POST['coupon_code']
        now = timezone.now()

        try:
            # Retrieve the coupon
            coupon = Coupon.objects.get(
                code=coupon_code,
                valid_from__lte=now,
                valid_to__gte=now,
                active=True
            )

            # Check if the user has already used the coupon
            if CouponUsage.objects.filter(user=request.user, coupon=coupon).exists():
                messages.error(request, "You have already used this coupon.")
            else:
                coupon_discount = coupon.discount
                final_total = (total + delivery_fee) * (1 - coupon_discount / 100)
                CouponUsage.objects.create(user=request.user, coupon=coupon)
                request.session['coupon_code'] = coupon_code
                messages.success(request, f"Coupon applied successfully! You received a {coupon_discount}% discount.")

        except Coupon.DoesNotExist:
            messages.error(request, "This coupon is invalid or expired.")

    return render(request, 'ecom/cart.html', {
        'products': products,
        'total': total,
        'delivery_fee': delivery_fee,
        'final_total': final_total,
        'product_count_in_cart': product_count_in_cart,
        'coupon_discount': coupon_discount,
        'cart': cart,  # Passing the cart to template
    })

# Remove from Cart View
def remove_from_cart_view(request, pk):
    # Initialize the cart from cookies
    if 'cart' in request.COOKIES:
        cart = json.loads(request.COOKIES['cart'])
    else:
        cart = {}

    # Remove or set the product quantity to 0
    if str(pk) in cart:
        if cart[str(pk)]['quantity'] > 1:
            cart[str(pk)]['quantity'] -= 1  # Decrease quantity if more than 1
        else:
            del cart[str(pk)]  # Remove product from cart completely if quantity is 1

    # Calculate the total price after removal
    total = sum(item['price'] * item['quantity'] for item in cart.values())

    # Update the cart cookie with the new value
    response = redirect('cart_view')  # Redirect to the cart view after removal
    response.set_cookie('cart', json.dumps(cart))  # Update the cart in cookies

    # Show success message
    messages.info(request, "Product removed from cart successfully!")

    return response

def send_feedback_view(request):
    feedbackForm=forms.FeedbackForm()
    if request.method == 'POST':
        feedbackForm = forms.FeedbackForm(request.POST)
        if feedbackForm.is_valid():
            feedbackForm.save()
            return render(request, 'ecom/feedback_sent.html')
    return render(request, 'ecom/send_feedback.html', {'feedbackForm':feedbackForm})


#_________________________________________
#___________Remove Coupon_________________
#__________________________________________


#---------------------------------------------------------------------------------
#------------------------ CUSTOMER RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_home_view(request):
    products=models.Product.objects.all()
    featured_categories = models.Category.objects.filter(featured=True)  # Only featured categories
    popular_products = models.Product.objects.filter(featured=True)
    categories = models.Category.objects.all()
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0
    return render(request,'ecom/customer_home.html',{'products':products,'product_count_in_cart':product_count_in_cart,'categories': categories,
        'featured_categories': featured_categories, 'popular_products': popular_products, })



# shipment address before placing order
@login_required(login_url='customerlogin')
def customer_address_view(request):
    # Check if products are present in the cart
    product_in_cart = False
    cart = {}

    if 'cart' in request.COOKIES:
        cart = json.loads(request.COOKIES.get('cart', '{}'))
        if cart:  # If the cart is not empty
            product_in_cart = True

    # Count total products in the cart
    product_count_in_cart = sum(item['quantity'] for item in cart.values()) if cart else 0

    addressForm = forms.AddressForm()

    if request.method == 'POST':
        addressForm = forms.AddressForm(request.POST)
        if addressForm.is_valid():
            # Collecting form data
            email = addressForm.cleaned_data['email']
            mobile = addressForm.cleaned_data['mobile']
            address_line_1 = addressForm.cleaned_data['address_line_1']

            # Calculate the total price of products in the cart
            total = 0
            product_ids_in_cart = cart.keys()
            products = models.Product.objects.filter(id__in=product_ids_in_cart)

            for p in products:
                total += p.price * cart[str(p.id)]['quantity']

            response = render(request, 'ecom/payment.html', {'total': total})
            response.set_cookie('email', email)
            response.set_cookie('mobile', mobile)
            response.set_cookie('address', address_line_1)
            return response

    return render(request, 'ecom/customer_address.html', {
        'addressForm': addressForm,
        'product_in_cart': product_in_cart,
        'product_count_in_cart': product_count_in_cart,
    })


# here we are just directing to this view...actually we have to check whther payment is successful or not
#then only this view should be accessed
@login_required(login_url='customerlogin')
def payment_success_view(request):
    customer = Customer.objects.get(user_id=request.user.id)
    products = None
    email = None
    mobile = None
    address = None

    # Get products from cookies
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        if product_ids:
            product_id_in_cart = product_ids.split('|')
            products = Product.objects.filter(id__in=product_id_in_cart)

    # Get customer details from cookies
    if 'email' in request.COOKIES:
        email = request.COOKIES['email']
    if 'mobile' in request.COOKIES:
        mobile = request.COOKIES['mobile']
    if 'address' in request.COOKIES:
        address = request.COOKIES['address']

    if products:
        # Create a new order (group)
        order = Order.objects.create(
            customer=customer,
        )

        # Create individual orders for each product
        for product in products:
            Orders.objects.create(
                customer=customer,
                product=product,
                order=order,
                email=email,
                mobile=mobile,
                address=address,
                status='Pending',
            )

        # Show the order number on the success page
        response = render(request, 'ecom/payment_success.html', {'order_number': order.order_number})

        # Clear the cookies
        response.delete_cookie('product_ids')
        response.delete_cookie('email')
        response.delete_cookie('mobile')
        response.delete_cookie('address')
        return response

    return render(request, 'ecom/payment_success.html', {'error': 'No products found in cart.'})



@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def my_order_view(request):
    
    customer=models.Customer.objects.get(user_id=request.user.id)
    orders=models.Orders.objects.all().filter(customer_id = customer)
    ordered_products=[]
    for order in orders:
        ordered_product=models.Product.objects.all().filter(id=order.product.id)
        ordered_products.append(ordered_product)

    return render(request,'ecom/my_order.html',{'data':zip(ordered_products,orders)})
 



# @login_required(login_url='customerlogin')
# @user_passes_test(is_customer)
# def my_order_view2(request):

#     products=models.Product.objects.all()
#     if 'product_ids' in request.COOKIES:
#         product_ids = request.COOKIES['product_ids']
#         counter=product_ids.split('|')
#         product_count_in_cart=len(set(counter))
#     else:
#         product_count_in_cart=0
#     return render(request,'ecom/my_order.html',{'products':products,'product_count_in_cart':product_count_in_cart})    



#--------------for discharge patient bill (pdf) download and printing
import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return

@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def download_invoice_view(request,orderID,productID):
    order=models.Orders.objects.get(id=orderID)
    product=models.Product.objects.get(id=productID)
    mydict={
        'orderDate':order.order_date,
        'customerName':request.user,
        'customerEmail':order.email,
        'customerMobile':order.mobile,
        'shipmentAddress':order.address,
        'orderStatus':order.status,

        'productName':product.name,
        'productImage':product.product_image,
        'productPrice':product.price,
        'productDescription':product.description,


    }
    return render_to_pdf('ecom/download_invoice.html',mydict)






@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def my_profile_view(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    
    # Fetch all active coupons
    now = timezone.now()
    active_coupons = Coupon.objects.filter(valid_from__lte=now, valid_to__gte=now, active=True)
    
    # Pass customer and active_coupons to the template
    return render(request, 'ecom/my_profile.html', {
        'customer': customer,
        'active_coupons': active_coupons
    })

@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def edit_profile_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    user=models.User.objects.get(id=customer.user_id)
    userForm=forms.CustomerUserForm(instance=user)
    customerForm=forms.CustomerForm(request.FILES,instance=customer)
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST,instance=user)
        customerForm=forms.CustomerForm(request.POST,instance=customer)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customerForm.save()
            return HttpResponseRedirect('my-profile')
    return render(request,'ecom/edit_profile.html',context=mydict)



#---------------------------------------------------------------------------------
#------------------------ ABOUT US AND CONTACT US VIEWS START --------------------
#---------------------------------------------------------------------------------
def aboutus_view(request):
    return render(request,'ecom/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message, settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'ecom/contactussuccess.html')
    return render(request, 'ecom/contactus.html', {'form':sub})


#__________________________________________________
#________________COUPON SYSTEM_____________________
#_________________________________________________
@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def apply_coupon(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST or None)
    
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(
                code=code,
                valid_from__lte=now,
                valid_to__gte=now,
                active=True
            )
            # Check if coupon is valid for this user
            if coupon.users.exists() and request.user not in coupon.users.all():
                # Invalid for this user
                return render(request, 'cart/invalid_coupon.html', {'error': 'Coupon not valid for your account'})
            
            # Apply the coupon (Store in session or cart model)
            request.session['coupon_id'] = coupon.id
            return redirect('cart_detail')

        except Coupon.DoesNotExist:
            return render(request, 'cart/invalid_coupon.html', {'error': 'Invalid coupon code'})

    return render(request, 'cart/apply_coupon.html', {'form': form})

#____________________________________________
#_____________CART COPUN_____________________
#_____________________________________________
@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def cart_detail(request):
    cart = request.session.get('cart', {})
    coupon_id = request.session.get('coupon_id')
    discount = 0
    coupon = None
    
    if coupon_id:
        coupon = get_object_or_404(Coupon, id=coupon_id)
        discount = coupon.discount

    total_price = sum(Decimal(item['price']) for item in cart.values())
    total_with_discount = total_price * (1 - discount / 100)
    
    return render(request, 'cart/cart_detail.html', {
        'cart': cart,
        'total_price': total_price,
        'discount': discount,
        'total_with_discount': total_with_discount,
        'coupon': coupon,
    })

def privacy_policy(request):
    return render(request, 'ecom/privacy_policy.html')

def terms_conditions(request):
    return render(request, 'ecom/terms&conditions.html')

def return_refund(request):
    return render(request, 'ecom/return&refund.html')

def contactus(request):
    return render(request, 'ecom/contactus.html')

def aboutus(request):
    return render(request, 'ecom/aboutus.html')

def shipping(request):
    return render(request, 'ecom/shiping.html')

def faq(request):
    return render(request, 'ecom/faq.html')



def product_list(request):
    product_list = Product.objects.all()  # Get all products
    paginator = Paginator(product_list, 3)  # Show 12 products per page
    
    # Get the current page number from the query parameters
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)  # Paginated products for the current page
    
    context = {
        'products': products,
    }
    return render(request, 'productlisht.html', context)


def all_categories_view(request):
    categories = Category.objects.all()  # Fetch all categories
    return render(request, 'ecom/allcategories.html', {'categories': categories})

def all_products_view(request):
    product = Product.objects.all()  # Fetch all categories
    return render(request, 'ecom/allproducts.html', {'products': product})


def product_detail(request, product_id, sub_category_id):

    product = get_object_or_404(Product, id=product_id)
    related_products = Product.objects.filter(sub_category=product.sub_category).exclude(id=product_id)[:4]  # Get related products

    # Fetch all products for the given sub-category


    # Group products by sub-category for the template
    sub_category_products = {
        sub_category_id: related_products
    }

    context = {
        'product': product,
        'related_products': related_products,  # Include grouped products
    }
    return render(request, 'ecom/viewmore.html', context)


def update_quantity(request, pk):
    # Check if cart exists in cookies
    if 'cart' in request.COOKIES:
        cart = json.loads(request.COOKIES['cart'])
    else:
        cart = {}

    # Update the quantity of the product
    if str(pk) in cart:
        quantity = request.POST.get('quantity', 1)
        cart[str(pk)]['quantity'] = int(quantity)

        # Update the cart in cookies
        response = redirect('cart')  # Assuming your cart view is named 'cart'
        response.set_cookie('cart', json.dumps(cart))

        # Show success message
        messages.info(request, "Product quantity updated successfully!")
        return response
    else:
        messages.error(request, "Product not found in cart.")
        return redirect('cart')
    

#____________________________________________
#________delivery____________________________
#_______________________________________________
def set_delivery_method(request):
    if request.method == 'POST':
        delivery_method = request.POST.get('delivery_method')
        if delivery_method:
            # Store the delivery method in session or database
            request.session['delivery_method'] = delivery_method
            messages.success(request, f"You selected {delivery_method.replace('_', ' ').title()} as your delivery method.")
        else:
            messages.error(request, "Please select a delivery method.")
    return redirect('cart')  # Redirect back to the cart page


 

