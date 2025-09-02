# contents/templatetags/text_extras.py
from django import template
from django.utils.html import conditional_escape, format_html_join
from django.utils.safestring import mark_safe

register = template.Library()

def _split_parts(value: str, sep: str):
    s = str(value or "")
    # спец-случай: передали "\n" строкой — трактуем как перевод строки
    if sep == r"\n":
        sep = "\n"
    parts = [p.strip() for p in s.replace("\r\n", "\n").split(sep)]
    return [p for p in parts if p]  # убираем пустые

@register.filter
def split_by(value, sep="|"):
    """Возвращает список строк, разделённых сепаратором (по умолчанию '|')."""
    return _split_parts(value, sep)

@register.filter
def to_spans(value, sep="|"):
    """
    Возвращает готовую HTML-разметку:
    <span class="line md:block">…</span>… для каждой части.
    """
    parts = _split_parts(value, sep)
    # экранируем содержимое, классы фиксируем, так безопаснее
    return format_html_join(
        "", '<span class="line md:block">{}</span>',
        ((conditional_escape(p),) for p in parts)
    )
