from django import template

register = template.Library()


@register.filter(name="get_array_element")
def get_array_element(array, index):
    return array[index]
