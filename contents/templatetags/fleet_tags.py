from django import template
from django.utils.translation import get_language
from ..models import FleetBlock

register = template.Library()

@register.inclusion_tag("contents/partials/_fleet_block.html", takes_context=True)
def fleet_block(context, slug):
    """
    Использование: {% load fleet_tags %} {% fleet_block "fleet-core" %}
    """
    request = context.get("request")
    block = (
        FleetBlock.objects
        .filter(slug=slug)
        .prefetch_related("items__specs")
        .first()
    )
    return {
        "request": request,
        "block": block,
        "LANGUAGE_CODE": get_language(),
    }
