from django import template

register = template.Library()

@register.filter
def format_currency(value, currency=''):
    try:
        value = float(value)
        return f'{currency} {value:,.2f}' if currency else f'{value:,.2f}'
    except (ValueError, TypeError):
        return f'{currency} {value}'