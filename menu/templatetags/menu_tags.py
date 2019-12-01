from django import template
from django.urls import resolve

from ..models import MenuItem
from ..utils import find_active, create_path, create_sequence

register = template.Library()


@register.inclusion_tag('menu/menu.html', takes_context=True)
def draw_menu(context, name):
    items = MenuItem.objects.filter(menu_name=name).values()
    request = context['request']

    current_url = resolve(request.path_info).url_name
    if current_url is None:
        current_url = request.build_absolute_uri()

    id_map, active = find_active(items, current_url)

    path = create_path(id_map, active)

    sequence = create_sequence(path)

    return {'sequence': sequence}


@register.simple_tag(takes_context=True)
def get_current_url(context):
    request = context['request']
    current_url = resolve(request.path_info).url_name

    return current_url


@register.filter
def get_value(obj, key):
    return obj[key]
