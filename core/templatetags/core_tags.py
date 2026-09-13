from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    if isinstance(dictionary, dict):
        return dictionary.get(str(key), dictionary.get(key, ''))
    return ''
