# contents/templatetags/social_tags.py
from django import template
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import get_language
from ..models import SocialLinksBlock, SocialLinksBlockPlacement

register = template.Library()

@register.inclusion_tag("contents/partials/_social_block.html", takes_context=True)
def social_block(context, slug, ul_class=None, icon_class=None, new_tab=True):
    """
    Рендер блока по слагу:
      {% social_block "social-core" %}
    Можно переопределить классы:
      {% social_block "social-core" ul_class="flex gap-6" icon_class="[&>svg]:h-8 [&>svg]:w-8" %}
    """
    request = context.get("request")
    block = (SocialLinksBlock.objects
             .filter(slug=slug)
             .prefetch_related("items")
             .first())
    return {
        "request": request,
        "block": block,
        "ul_class": ul_class,
        "icon_class": icon_class,
        "new_tab": new_tab,
        "LANGUAGE_CODE": get_language(),
    }

@register.inclusion_tag("contents/partials/_social_blocks_for.html", takes_context=True)
def social_blocks_for(context, page_obj, ul_class=None, icon_class=None, new_tab=True):
    """
    Рендер всех блоков соцсетей, прикреплённых к странице (через placements):
      {% social_blocks_for page %}
    """
    request = context.get("request")
    if not page_obj or not getattr(page_obj, "pk", None):
        return {"request": request, "placements": [], "ul_class": ul_class, "icon_class": icon_class, "new_tab": new_tab}
    ct = ContentType.objects.get_for_model(page_obj.__class__)
    placements = (SocialLinksBlockPlacement.objects
                  .select_related("block")
                  .filter(page_content_type=ct, page_object_id=page_obj.pk)
                  .prefetch_related("block__items")
                  .order_by("order", "id"))
    return {
        "request": request,
        "placements": placements,
        "ul_class": ul_class,
        "icon_class": icon_class,
        "new_tab": new_tab,
        "LANGUAGE_CODE": get_language(),
    }
