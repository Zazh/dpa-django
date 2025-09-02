# contents/templatetags/faq_tags.py
from django import template
from django.utils.translation import get_language
from django.apps import apps

register = template.Library()

@register.inclusion_tag("contents/partials/_faq_block.html", takes_context=True)
def faq_block(context, slug):
    request = context.get("request")
    FaqBlock = apps.get_model("contents", "FaqBlock")
    block = None
    if FaqBlock is not None:
        block = (FaqBlock.objects
                 .prefetch_related("items")
                 .filter(slug=slug)
                 .first())
    return {"request": request, "block": block, "LANGUAGE_CODE": get_language()}
