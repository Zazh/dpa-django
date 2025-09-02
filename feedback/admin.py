from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TabbedTranslationAdmin
from .models import FeedbackAction, FeedbackSubmission

@admin.register(FeedbackAction)
class FeedbackActionAdmin(TabbedTranslationAdmin):
    list_display = ("slug", "label", "updated")
    search_fields = ("slug", "label")
    fields = (
        "slug",
        "label_ru", "label_kk", "label_en",
        "modal_title_ru", "modal_title_kk", "modal_title_en",
        "submit_label_ru", "submit_label_kk", "submit_label_en",
        "name_label_ru", "name_label_kk", "name_label_en",
        "phone_label_ru", "phone_label_kk", "phone_label_en",
        "success_message_ru", "success_message_kk", "success_message_en",
    )

@admin.register(FeedbackSubmission)
class FeedbackSubmissionAdmin(admin.ModelAdmin):
    list_display  = ("created", "action", "name", "phone", "page", "locale")
    list_filter   = ("action", "locale", "created")
    search_fields = ("name", "phone", "page")
    readonly_fields = ("created",)
