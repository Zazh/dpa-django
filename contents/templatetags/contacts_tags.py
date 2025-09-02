# contents/templatetags/contacts_tags.py (новый файл)
from django import template
from django.utils.translation import get_language
from ..models import ContactPage

register = template.Library()

@register.inclusion_tag("contents/partials/_contacts_footer.html", takes_context=True)
def contact_footer(context):
    """
    Использование: {% load contacts_tags %} {% contact_footer %}
    Безопасно: если ContactPage отсутствует — ничего не выводим.
    """
    request = context.get("request")
    page = ContactPage.objects.first()
    return {
        "request": request,
        "page": page,
        "LANGUAGE_CODE": get_language(),
    }
