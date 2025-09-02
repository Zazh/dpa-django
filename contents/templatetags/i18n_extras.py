from django import template
from django.urls import translate_url as _translate_url

register = template.Library()

@register.filter(name="translate_url")
def translate_url_filter(path_or_url: str, lang_code: str) -> str:
    try:
        return _translate_url(path_or_url, lang_code)
    except Exception:
        return path_or_url
