# contents/templatetags/gallery_tags.py
from django import template
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import get_language
from ..models import GalleryBlock, GalleryBlockPlacement

register = template.Library()

@register.inclusion_tag("contents/partials/_gallery_block.html", takes_context=True)
def gallery_block(context, slug):
    request = context.get("request")
    block = (GalleryBlock.objects
             .filter(slug=slug)
             .prefetch_related("items")
             .first())
    return {"request": request, "block": block, "LANGUAGE_CODE": get_language()}

@register.inclusion_tag("contents/partials/_gallery_blocks_for.html", takes_context=True)
def gallery_blocks_for(context, page_obj):
    request = context.get("request")
    if not page_obj or not getattr(page_obj, "pk", None):
        return {"request": request, "placements": [], "LANGUAGE_CODE": get_language()}
    ct = ContentType.objects.get_for_model(page_obj.__class__)
    placements = (GalleryBlockPlacement.objects
                  .select_related("block")
                  .filter(page_content_type=ct, page_object_id=page_obj.pk)
                  .prefetch_related("block__items")
                  .order_by("order", "id"))
    return {"request": request, "placements": placements, "LANGUAGE_CODE": get_language()}
