# contents/templatetags/benefits_tags.py
from django import template
from django.db.utils import ProgrammingError, OperationalError
from ..models import BenefitSection

register = template.Library()

@register.inclusion_tag("contents/partials/_benefit_sections.html", takes_context=True)
def benefits_block(context, slug):
    """
    Рендер секции бенефитов по slug:
      {% benefits_block "home-benefits" %}
    Использует существующий партиал, который ждёт sections (список).
    """
    request = context.get("request")
    try:
        section = (
            BenefitSection.objects
            .filter(slug=slug)
            .prefetch_related("items")
            .first()
        )
    except (ProgrammingError, OperationalError):
        section = None

    return {
        "request": request,
        "sections": [section] if section else [],
    }
