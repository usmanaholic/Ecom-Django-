from django.contrib import admin
from .models import Customer, Order,Product,Feedback,Category, Sub_category, Color, banner, HeroSection, HeroSectionImage
from .models import Coupon
# Register your models here.
class CustomerAdmin(admin.ModelAdmin):
    pass
admin.site.register(Customer, CustomerAdmin)

class ProductAdmin(admin.ModelAdmin):
    pass
admin.site.register(Product, ProductAdmin)

class OrderAdmin(admin.ModelAdmin):
    pass
admin.site.register(Order, OrderAdmin)

class FeedbackAdmin(admin.ModelAdmin):
    pass
admin.site.register(Feedback, FeedbackAdmin)
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'featured')
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Color)

admin.site.register(Sub_category)
#COPUN
@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount', 'valid_from', 'valid_to', 'active']
    list_filter = ['active', 'valid_from', 'valid_to']
    search_fields = ['code']

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer', 'total_price', 'status')



class OrderAdmin(admin.ModelAdmin):
    search_fields = ['order_number', 'customer__name']




admin.site.register(banner)


@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'button_text')


admin.site.register(HeroSectionImage)