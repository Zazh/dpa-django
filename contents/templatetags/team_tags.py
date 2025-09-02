# contents/templatetags/team_tags.py  (новый файл; не забудь __init__.py)
from django import template
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import get_language
from ..models import TeamBlock, TeamBlockPlacement

register = template.Library()

@register.inclusion_tag("contents/partials/_team_block.html", takes_context=True)
def team_block(context, slug):
    request = context.get("request")
    block = TeamBlock.objects.filter(slug=slug).prefetch_related("members").first()
    return {"request": request, "block": block, "LANGUAGE_CODE": get_language()}

@register.inclusion_tag("contents/partials/_team_blocks_for.html", takes_context=True)
def team_blocks_for(context, page_obj):
    request = context.get("request")
    if not page_obj or not getattr(page_obj, "pk", None):
        return {"request": request, "placements": [], "LANGUAGE_CODE": get_language()}
    ct = ContentType.objects.get_for_model(page_obj.__class__)
    placements = (TeamBlockPlacement.objects
                  .select_related("block")
                  .filter(page_content_type=ct, page_object_id=page_obj.pk)
                  .prefetch_related("block__members")
                  .order_by("order", "id"))
    return {"request": request, "placements": placements, "LANGUAGE_CODE": get_language()}
