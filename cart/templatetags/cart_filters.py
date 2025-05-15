from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()

@register.filter
def currency(value):
    try:
        value = int(value)
        return "Rp{}".format(intcomma(value))
    except:
        return value
@register.filter
def mul(value, arg):
    try:
        return int(value) * int(arg)
    except:
        return 0
    
@register.filter
def div(value, arg):
    try:
        return int(value) / int(arg)
    except:
        return 0

@register.filter
def cart_total(cart_items):
    return sum(item.price * item.quantity for item in cart_items)

