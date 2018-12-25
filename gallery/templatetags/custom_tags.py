from django import template
register = template.Library()

@register.simple_tag
def active(request, pattern):
    #import re
    #if re.search(pattern, request.path):
    #    return 'active'
    #return ''
    return 'active' if pattern == request.path else ''

@register.filter
def sort_by(queryset, order):
    return queryset.order_by(order)

@register.filter
def key_to_list(queryset, key):
    return queryset.values_list(key, flat=True)
