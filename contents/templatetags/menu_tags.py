# contents/templatetags/menu_tags.py
from django import template
from django.urls import reverse, NoReverseMatch
from django.utils.translation import get_language
from django.conf import settings
from urllib.parse import urlparse

from ..models import MenuItem

register = template.Library()

@register.simple_tag
def menu_items(slug):
    return (MenuItem.objects
            .filter(menu__slug=slug, visible=True)
            .order_by("order", "id"))

@register.simple_tag
def menu_href(item: MenuItem) -> str:
    if item.url_name:
        try:
            return reverse(item.url_name)   # поддерживает namespace: 'blog:list'
        except NoReverseMatch:
            return "#"
    return item.url_path or "#"

def _strip_lang_prefix(path: str) -> str:
    """Уберём языковой префикс (/en/, /kk/) для сравнения путей."""
    if not path:
        return "/"
    lang = (get_language() or "").split("-")[0]
    default = (settings.LANGUAGE_CODE or "ru").split("-")[0]
    prefix = f"/{lang}/"
    if lang and lang != default and path.startswith(prefix):
        rest = path[len(prefix):]
        return "/" + rest  # вернуть с ведущим слэшем
    return path

def _norm(p: str) -> str:
    """Нормализация: ведущий + конечный слэш для сравнения разделов."""
    if not p:
        return "/"
    if not p.startswith("/"):
        p = "/" + p
    if not p.endswith("/"):
        p = p + "/"
    return p

@register.simple_tag(takes_context=True)
def menu_is_active(context, item: MenuItem, mode: str = "section") -> bool:
    """
    mode='section' — подсветка для раздела и всех вложенных путей (по умолчанию)
    mode='exact'   — точное совпадение пути
    """
    request = context.get("request")
    if not request:
        return False

    current = _norm(_strip_lang_prefix(request.path))

    # URL для пункта
    if item.url_name:
        try:
            href = reverse(item.url_name)
        except NoReverseMatch:
            return False
    else:
        href = item.url_path or ""

    # Внешние ссылки никогда не активны
    parsed = urlparse(href)
    if parsed.scheme in ("http", "https"):
        return False

    target = _norm(_strip_lang_prefix(href))

    if mode == "exact":
        return current == target

    # section-режим: активен на самом пути и на подпутях
    return current == target or (target != "/" and current.startswith(target))
