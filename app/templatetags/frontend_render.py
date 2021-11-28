from django import template
from html.parser import HTMLParser
import re

register = template.Library()

@register.filter
def replaceSpace(value):
    return value.replace(' ','-')
   