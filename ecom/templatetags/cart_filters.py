from django import template

register = template.Library()

@register.filter
def get_item(cart, product_id):
    # Retrieve the quantity of the product from the cart
    return cart.get(str(product_id), {}).get('quantity', 0)