from django import template
from django.template.defaultfilters import stringfilter
register = template.Library()
@register.filter
@stringfilter
def explode(value: [str], separator):
    return value.split(separator)
