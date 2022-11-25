from django import template
from django.shortcuts import render

"""
Custom template tags for the saratingsapp
https://youtu.be/9dryekIFiSw
"""

register = template.Library()

def render_subscription_type(subscription_type):
    if "unsub" in subscription_type:
        return subscription_type
    else:
        return subscription_type.replace('_',"-") +" "+"Subscription"
        

def render_subscription_item(subscription_item):
    return subscription_item.replace('_'," ")

def render_subscription_item_fee(subscription_item_fee):
    
    if subscription_item_fee == 'free' or subscription_item_fee == 'full_access' or subscription_item_fee == 'free_+_vip_access_to_sar_team':
        return " - "+render_subscription_item(subscription_item_fee)
    else:
        return "- zar {:,.2f}".format(float(subscription_item_fee))
    

def render_currency(value):
    return "zar {:,.2f}".format(float(value))

register.filter('render_subscription_type', render_subscription_type)
register.filter('render_subscription_item', render_subscription_item)
register.filter('render_subscription_item_fee', render_subscription_item_fee)
register.filter('render_currency', render_currency)