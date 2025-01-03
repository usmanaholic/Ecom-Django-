from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(str(key))


import json
from django import template

register = template.Library()

@register.filter
def json_query(cart, key):
    """
    Queries a JSON-like dictionary (passed as a string) and retrieves the value for the given key.
    """
    try:
        cart_data = json.loads(cart)
        return cart_data.get(str(key), {}).get('quantity', 0)
    except (json.JSONDecodeError, AttributeError):
        return 0
