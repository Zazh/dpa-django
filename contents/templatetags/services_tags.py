# contents/templatetags/services_tags.py
from django import template
from django.utils.translation import get_language
from ..models import ServicePage

register = template.Library()

@register.inclusion_tag("contents/partials/_services_block.html", takes_context=True)
def services_cards(context, limit=None):
    """
    Выводит карточки из ServicePage по флагу show=True.
    Использование: {% services_cards %} или {% services_cards 6 %}
    """
    request = context.get("request")
    qs = (ServicePage.objects
          .filter(show=True)
          .order_by("services_order", "id")
          .only("slug", "title", "subtitle", "card_icon_svg", "card_tags_text"))
    if limit:
        try:
            limit = int(limit)
            qs = qs[:limit]
        except (ValueError, TypeError):
            pass

    pages = list(qs)
    return {
        "request": request,
        "pages": pages,
        "LANGUAGE_CODE": get_language(),
    }

# ВРЕМЕННЫЙ алиас для обратной совместимости со старыми шаблонами
@register.inclusion_tag("contents/partials/_services_block.html", takes_context=True)
def services_block(context, slug="categories"):
    # игнорируем slug, просто рендерим список ServicePage
    return services_cards(context)
