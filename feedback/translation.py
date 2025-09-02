from modeltranslation.translator import TranslationOptions, register
from .models import FeedbackAction

@register(FeedbackAction)
class FeedbackActionTR(TranslationOptions):
    fields = (
        "label",
        "modal_title",
        "submit_label",
        "name_label",
        "phone_label",
        "success_message",
    )
