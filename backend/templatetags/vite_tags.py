from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def vite_asset(path):
    if settings.VITE_DEV_MODE:
        return f'{settings.VITE_DEV_SERVER_URL}{path}'
    return f'{settings.STATIC_URL}dist/{path}'