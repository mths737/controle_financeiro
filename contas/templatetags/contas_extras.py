from django import template

register = template.Library()

@register.inclusion_tag("partials/ordenar_th.html")
def ordenar_th(label, field, order_by, order):
    return {
        "label": label,
        "field": field,
        "order_by": order_by,
        "order": order,
    }