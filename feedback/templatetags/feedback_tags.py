from django import template
from django.urls import reverse
from django.utils.translation import get_language
from ..models import FeedbackAction

register = template.Library()

@register.inclusion_tag("feedback/modal.html", takes_context=True)
def feedback_modal(context, default_slug="callback"):
    request = context.get("request")
    action = FeedbackAction.objects.filter(slug=default_slug).first()
    return {
        "request": request,
        "action": action,
        "action_slug": action.slug if action else "",
        "label": action.label if action else "Отправить заявку",
        "modal_title": action.modal_title if action else "Заявка",
        "submit_label": action.submit_label if action else "Отправить",
        "name_label": action.name_label if action else "Имя",
        "phone_label": action.phone_label if action else "Телефон",
        "success_message": action.success_message if action else "Спасибо! Мы свяжемся с вами.",
        "post_url": reverse("feedback_submit"),
        "LANGUAGE_CODE": get_language(),
    }

@register.inclusion_tag("feedback/button_wrapper.html", takes_context=True)
def feedback_button(context, slug, variant="solid", css_class="", label_override=None):
    request = context.get("request")
    action = FeedbackAction.objects.filter(slug=slug).first()
    button_templates = [
        f"feedback/buttons/{variant}.html",
        "feedback/buttons/solid.html",
    ]
    return {
        "request": request,
        "action": action,
        "css_class": css_class,
        "label": label_override or (action.label if action else "Отправить заявку"),
        "modal_title": (action.modal_title if action else ""),
        "submit_label": (action.submit_label if action else ""),
        "name_label": (action.name_label if action else "Имя"),
        "phone_label": (action.phone_label if action else "Телефон"),
        "button_templates": button_templates,
    }
