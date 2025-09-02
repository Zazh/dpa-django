# blog/templatetags/markup.py  (или blog_markup.py — в зависимости от имени)
from django import template
from django.utils.safestring import mark_safe
import markdown as md
import bleach

register = template.Library()

ALLOWED_TAGS = [
    "p", "br", "ul", "ol", "li",
    "strong", "em", "blockquote", "code", "pre",
    "a", "h2", "h3", "h4", "hr"
]
ALLOWED_ATTRS = {
    "a": ["href", "title", "rel", "target"],
}
ALLOWED_PROTOCOLS = ["http", "https", "mailto"]

@register.filter(name="markdown_safe", is_safe=True)
def markdown_safe(value):
    if not value:
        return ""
    html = md.markdown(
        value,
        extensions=["extra", "sane_lists", "smarty"],
        output_format="html5",
    )
    clean = bleach.clean(
        html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRS,
        protocols=ALLOWED_PROTOCOLS,
        strip=True,
    )
    # при желании: bleach.linkify(clean) чтобы авто-ссылки работали
    return mark_safe(clean)  # <- ключевая строка
