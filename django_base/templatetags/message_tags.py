from django import template

register = template.Library()


@register.simple_tag
def message_class(tag):
    if tag == "info":
        return "positive"
    return ""
