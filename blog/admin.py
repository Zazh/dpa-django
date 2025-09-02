from django.contrib import admin
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TabbedTranslationAdmin
from .models import BlogPost, BlogSettings


@admin.register(BlogPost)
class BlogPostAdmin(TabbedTranslationAdmin):
    list_display = ("__str__", "is_published", "published_at", "updated")
    list_filter = ("is_published",)
    search_fields = ("slug", "title_ru", "title_en", "title_kk", "subtitle_ru", "subtitle_en", "subtitle_kk", "tags_text")
    ordering = ("-published_at", "-id")

    fieldsets = (
        (_("Header"), {
            "fields": (
                "slug",
                "title_ru", "title_kk", "title_en",
                "subtitle_ru", "subtitle_kk", "subtitle_en",
                "author", "published_at", "is_published",
                "tags_text", "image",
            )
        }),
        (_("Body"), {"fields": ("body_md_ru", "body_md_kk", "body_md_en")}),
        (_("SEO"), {
            "fields": (
                "meta_title_ru", "meta_title_kk", "meta_title_en",
                "meta_description_ru", "meta_description_kk", "meta_description_en",
            )
        }),
    )

    def get_prepopulated_fields(self, request, obj=None):
        lang = getattr(settings, "MODELTRANSLATION_DEFAULT_LANGUAGE", None) \
               or getattr(settings, "LANGUAGE_CODE", "ru").split("-")[0]
        return {"slug": (f"title_{lang}",)}

@admin.register(BlogSettings)
class BlogSettingsAdmin(TabbedTranslationAdmin):
    list_display = ("__str__",)
    fields = ("title", "meta_title", "meta_description", "meta_keywords")
