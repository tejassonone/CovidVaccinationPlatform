from django import template
from ..models import Beneficiary

register = template.Library()

@register.simple_tag
def total_beneficiary():
    return Beneficiary.count()