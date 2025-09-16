# contents/templatetags/fleet_tags.py
from django import template
from django.utils.translation import get_language
from ..models import FleetBlock, FleetItem

register = template.Library()

@register.inclusion_tag("contents/partials/_fleet_items.html", takes_context=True)
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
        "items": list(block.items.all()) if block else [],
        "LANGUAGE_CODE": get_language(),
        "character_label": block.character_label if block else "",
        "block_title": block.title if block else "",
    }

@register.inclusion_tag("contents/partials/_fleet_items.html", takes_context=True)
def fleet_items(context, limit=None):
    """
    Показывает каталог авиапарка без всяких блоков.
    Использование: {% load fleet_tags %} {% fleet_items %} или {% fleet_items 12 %}
    """
    request = context.get("request")
    qs = (
        FleetItem.objects
        .select_related("block")
        .prefetch_related("specs")
        .order_by("order", "id")
    )
    if limit:
        try:
            qs = qs[:int(limit)]
        except (ValueError, TypeError):
            pass

    return {
        "request": request,
        "items": list(qs),
        "LANGUAGE_CODE": get_language(),
        # Локализуем подпись к характеристикам: берём из блока первого айтема, если есть
        "character_label": (qs[0].block.character_label if qs and qs[0].block and qs[0].block.character_label else "Характеристики"),
        "block_title": "",  # заголовок опционально
    }
