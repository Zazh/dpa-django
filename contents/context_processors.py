# contents/context_processors.py
from .models import ContactPage

def contacts_footer(request):
    """
    Кладёт в контекст объект ContactPage как `contacts_footer`.
    Безопасно: если записи нет — вернёт None.
    """
    return {"contacts_footer": ContactPage.objects.first()}
