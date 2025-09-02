from django.conf import settings
from django.contrib import admin
from django import forms
from django.urls import get_resolver, reverse, NoReverseMatch
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.admin import GenericTabularInline
from modeltranslation.admin import (
    TabbedTranslationAdmin,
    TranslationTabularInline,
    TranslationStackedInline,
)
from .models import HomePage, AboutPage, BenefitSection, BenefitItem, TeamBlock, TeamBlockPlacement, TeamMember, \
    PartnersBlock, PartnerLogo, \
    PartnersBlockPlacement, GalleryBlock, GalleryItem, GalleryBlockPlacement, SocialLinkItem, SocialLinksBlock, \
    SocialLinksBlockPlacement, Menu, MenuItem, ServicePage, ServiceSlide, ServiceBenefit, \
    ServiceAdvantage, ServiceProgramItem, FleetSpec, FleetItem, FleetBlock, FaqBlock, FaqItem, ContactPage


# ---- Team -----

class TeamMemberInline(TranslationTabularInline):
    model = TeamMember
    extra = 0
    fields = ("order", "name", "post", "description", "photo")
    ordering = ("order",)
    show_change_link = True

# ---- Partner -----

class PartnerLogoInline(admin.TabularInline):
    model = PartnerLogo
    extra = 0
    fields = ("order", "svg_code")
    ordering = ("order",)
    show_change_link = True

@admin.register(PartnersBlock)
class PartnersBlockAdmin(TabbedTranslationAdmin):
    list_display = ("__str__", "slug", "order", "updated")
    search_fields = ("slug", "title")
    fields = ("slug", "order", "title")
    readonly_fields = ("updated",)
    inlines = [PartnerLogoInline]

# Inline для привязок — подключай к страницам, если хочешь управлять показом через placements
class PartnersBlockPlacementInline(GenericTabularInline):
    model = PartnersBlockPlacement
    ct_field = "page_content_type"
    ct_fk_field = "page_object_id"
    extra = 0
    fields = ("block", "order")
    ordering = ("order",)
    autocomplete_fields = ("block",)

@admin.register(TeamBlock)
class TeamBlockAdmin(TabbedTranslationAdmin):
    list_display = ("__str__", "slug", "order", "updated")
    search_fields = ("slug", "title")
    fields = ("slug", "order", "title",)
    readonly_fields = ("updated",)
    inlines = [TeamMemberInline]

class TeamBlockPlacementInline(GenericTabularInline):
    model = TeamBlockPlacement
    ct_field = "page_content_type"
    ct_fk_field = "page_object_id"
    extra = 0
    fields = ("block", "order")
    ordering = ("order",)
    autocomplete_fields = ("block",)

# ---- Gallery ------
class GalleryItemInline(admin.TabularInline):
    model = GalleryItem
    extra = 0
    fields = ("order", "image", "alt")
    ordering = ("order",)
    show_change_link = True

@admin.register(GalleryBlock)
class GalleryBlockAdmin(TabbedTranslationAdmin):
    list_display = ("__str__", "slug", "order", "updated")
    search_fields = ("slug", "title")
    fields = ("slug", "order", "title")
    readonly_fields = ("updated",)
    inlines = [GalleryItemInline]

class GalleryBlockPlacementInline(GenericTabularInline):
    model = GalleryBlockPlacement
    ct_field = "page_content_type"
    ct_fk_field = "page_object_id"
    extra = 0
    fields = ("block", "order")
    ordering = ("order",)
    autocomplete_fields = ("block",)

# ---- Model admins ----

@admin.register(HomePage)
class HomePageAdmin(TabbedTranslationAdmin):
    list_display = ("__str__",)
    inlines = []
    fieldsets = (
        (_("Hero"), {"fields": ("hero_title", "hero_subtitle", "mission_text", "education_title")}),
        (_("Meta"), {"fields": ("meta_title", "meta_description")}),
    )

@admin.register(AboutPage)
class AboutPageAdmin(TabbedTranslationAdmin):
    list_display = ("__str__",)
    inlines = []
    fieldsets = (
        (_("Main"), {"fields": ("title", "subtitle", "mission_text", "education_title")}),
        (_("Meta"), {"fields": ("meta_title", "meta_description")}),
    )

class BenefitItemInline(TranslationTabularInline):
    model = BenefitItem
    extra = 0
    fields = ("order", "label", "detail")
    ordering = ("order",)
    show_change_link = True

@admin.register(BenefitSection)
class BenefitSectionAdmin(TabbedTranslationAdmin):
    list_display = ("__str__", "slug", "order")
    search_fields = ("title", "slug")
    fields = ("slug", "order", "title")
    inlines = [BenefitItemInline]

@admin.register(BenefitItem)
class BenefitItemAdmin(TabbedTranslationAdmin):
    list_display = ("__str__", "section", "order")
    list_filter = ("section",)
    search_fields = ("label", "detail")
    fields = ("section", "order", "label", "detail")

@admin.register(PartnersBlockPlacement)
class PartnersBlockPlacementAdmin(admin.ModelAdmin):
    list_select_related = ("block", "page_content_type",)
    list_display = ("block", "page", "order")
    list_filter = ("page_content_type",)
    search_fields = ("block__slug", "block__title")
    ordering = ("page_content_type", "page_object_id", "order", "id")
    autocomplete_fields = ("block",)

# ---- Social ------
class SocialLinkItemInline(admin.TabularInline):
    model = SocialLinkItem
    extra = 0
    fields = ("order", "label", "url", "svg_code")
    ordering = ("order",)
    show_change_link = True

@admin.register(SocialLinksBlock)
class SocialLinksBlockAdmin(TabbedTranslationAdmin):
    list_display = ("__str__", "slug", "order", "updated")
    search_fields = ("slug", "title")
    fields = ("slug", "order", "title")
    readonly_fields = ("updated",)
    inlines = [SocialLinkItemInline]

class SocialLinksBlockPlacementInline(GenericTabularInline):
    model = SocialLinksBlockPlacement
    ct_field = "page_content_type"
    ct_fk_field = "page_object_id"
    extra = 0
    fields = ("block", "order")
    ordering = ("order",)
    autocomplete_fields = ("block",)

@admin.register(SocialLinksBlockPlacement)
class SocialLinksBlockPlacementAdmin(admin.ModelAdmin):
    list_select_related = ("block", "page_content_type",)
    list_display = ("block", "page", "order")
    list_filter = ("page_content_type",)
    search_fields = ("block__slug", "block__title")
    ordering = ("page_content_type", "page_object_id", "order", "id")
    autocomplete_fields = ("block",)

def get_named_url_choices():
    from django.urls import get_resolver, NoReverseMatch, reverse
    names = sorted(n for n in get_resolver().reverse_dict.keys() if isinstance(n, str))
    choices = [("", "— выбрать по имени из urls —")]
    for n in names:
        try:
            reverse(n)  # отсекаем те, что требуют args/kwargs
            choices.append((n, n))
        except NoReverseMatch:
            pass
    return choices


class MenuItemForm(forms.ModelForm):
    url_name = forms.ChoiceField(choices=[], required=False, label="URL name (reverse)")

    class Meta:
        model = MenuItem
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["url_name"].choices = get_named_url_choices()

    def clean(self):
        cleaned = super().clean()
        url_name = cleaned.get("url_name")
        url_path = cleaned.get("url_path")

        if not url_name and not url_path:
            raise ValidationError("Укажи либо URL name, либо Path/URL.")
        if url_name and url_path:
            raise ValidationError("Заполняй только одно: URL name ИЛИ Path/URL.")

        if url_name:
            try:
                reverse(url_name)  # проверяем, что имя реально есть в urls.py
            except NoReverseMatch:
                raise ValidationError(f"URL name '{url_name}' не найден в urls.py.")
        return cleaned

@admin.register(Menu)
class MenuAdmin(TabbedTranslationAdmin):
    list_display = ("__str__", "slug", "updated")
    fields = ("slug", "title")

@admin.register(MenuItem)
class MenuItemAdmin(TabbedTranslationAdmin):
    form = MenuItemForm
    list_select_related = ("menu",)
    list_display = ("title", "menu", "order", "visible", "url_name", "url_path", "resolved_href")
    list_filter = ("menu", "visible")
    search_fields = ("title", "url_name", "url_path")
    ordering = ("menu", "order", "id")
    fields = ("menu", "order", "visible", "title", "url_name", "url_path", "open_in_new_tab")

    def resolved_href(self, obj):
        try:
            if obj.url_name:
                return reverse(obj.url_name)
            return obj.url_path or ""
        except NoReverseMatch:
            return "— invalid url_name —"
    resolved_href.short_description = "Resolved URL"


class ServiceSlideInline(admin.TabularInline):
    model = ServiceSlide
    extra = 0
    fields = ("order", "image", "alt")
    ordering = ("order",)

class ServiceBenefitInline(TranslationTabularInline):
    model = ServiceBenefit
    extra = 0
    fields = ("order", "name", "value")
    ordering = ("order",)

class ServiceAdvantageInline(TranslationTabularInline):
    model = ServiceAdvantage
    extra = 0
    fields = ("order", "icon_svg", "text")
    ordering = ("order",)

class ServiceProgramItemInline(TranslationStackedInline):
    model = ServiceProgramItem
    extra = 0
    fields = ("order", "anchor", "title", "time", "subtitle", "list_text")
    ordering = ("order",)
    show_change_link = True

@admin.register(ServiceProgramItem)
class ServiceProgramItemAdmin(TabbedTranslationAdmin):
    list_display = ("__str__", "page", "order")
    list_filter = ("page",)
    search_fields = ("title", "subtitle")
    fieldsets = (
        (_("Base"), {"fields": ("page", "order", "anchor", "title", "time", "subtitle", "list_text",)}),
        (_("Images"), {"fields": ("image1", "image2", "image3")}),
    )


@admin.register(ServicePage)
class ServicePageAdmin(TabbedTranslationAdmin):
    list_display = ("__str__", "slug", "show", "services_order", "updated")
    list_filter = ("show",)
    prepopulated_fields = {"slug": ("card_title_text",)}
    search_fields = ("slug", "title_ru", "title_en", "title_kk")
    ordering = ("services_order", "id")

    fieldsets = (
        (_("Card"), {
            "fields": (
                "show", "services_order",
                "card_title_text", "card_description_text",
                "card_icon_svg", "card_tags_text",
            )
        }),
        (_("Header"), {
            "fields": (
                "slug",
                "title_ru", "title_kk", "title_en",
                "subtitle_ru", "subtitle_kk", "subtitle_en",
                "program_title",
            )
        }),
        (_("SEO"), {
            "fields": (
                "meta_title_ru", "meta_title_kk", "meta_title_en",
                "meta_description_ru", "meta_description_kk", "meta_description_en",
            )
        }),
        (_("CTA"), {
            "fields": (
                "cta_title", "cta_descr",
            )
        }),
    )

    inlines = [
        ServiceSlideInline,
        ServiceBenefitInline,
        ServiceAdvantageInline,
        ServiceProgramItemInline,
    ]

class FleetSpecInline(TranslationTabularInline):
    model = FleetSpec
    extra = 0
    fields = ("order", "key", "value")
    ordering = ("order",)

@admin.register(FleetItem)
class FleetItemAdmin(TabbedTranslationAdmin):
    list_select_related = ("block",)
    list_display = ("__str__", "block", "order")
    list_filter  = ("block",)
    ordering     = ("block", "order", "id")
    fieldsets = (
        (_("Base"), {"fields": ("block", "order", "name", "subtitle", "description", "image")}),
    )
    inlines = [FleetSpecInline]

class FleetItemInline(TranslationTabularInline):
    model = FleetItem
    extra = 0
    fields = ("order", "name", "subtitle", "image")
    ordering = ("order",)
    show_change_link = True  # чтобы зайти и добавить specs

@admin.register(FleetBlock)
class FleetBlockAdmin(TabbedTranslationAdmin):
    list_display = ("__str__", "slug", "order", "updated")
    search_fields = ("slug", "title")
    fields = ("slug", "order", "title", "character_label")
    inlines = [FleetItemInline]
    readonly_fields = ("updated",)


#--- FAQ -----

class FaqItemInline(TranslationTabularInline):
    model = FaqItem
    extra = 0
    fields = ("order", "question", "answer")
    ordering = ("order",)
    show_change_link = True


@admin.register(FaqBlock)
class FaqBlockAdmin(TabbedTranslationAdmin):
    list_display = ("__str__", "slug", "order", "updated", "items_count", "cta_faq")
    search_fields = ("slug", "title", "cta_faq")

    # Явно показываем slug/order и переводимые поля title/cta_faq — указываем именно базовые имена,
    # TabbedTranslationAdmin сам разложит их по вкладкам языков.
    fields = ("slug", "order", "title", "cta_faq")

    inlines = [FaqItemInline]

    def get_prepopulated_fields(self, request, obj=None):
        from django.conf import settings
        lang = getattr(settings, "MODELTRANSLATION_DEFAULT_LANGUAGE", "ru")
        return {"slug": (f"title_{lang}",)}

    def items_count(self, obj):
        return obj.items.count()
    items_count.short_description = "Items"

@admin.register(FaqItem)
class FaqItemAdmin(TabbedTranslationAdmin):
    list_select_related = ("block",)
    list_display = ("__str__", "block", "order")
    list_filter = ("block",)
    search_fields = ("question", "answer")
    fields = ("block", "order", "question", "answer")
    ordering = ("block", "order", "id")


@admin.register(ContactPage)
class ContactPageAdmin(TabbedTranslationAdmin):
    list_display = ("__str__", "updated")
    fieldsets = (
        (_("Header"), {"fields": ("title", "subtitle")}),
        (_("Phone"), {"fields": ("phone_label", "phone_number")}),
        (_("Email"), {"fields": ("email_label", "email")}),
        (_("Address"), {"fields": ("address_label", "address_text", "address_url")}),
        (_("Footer"), {"fields": ("footer_text",)}),
        (_("SEO"), {"fields": ("meta_title", "meta_description")}),
    )

    # хотим лишь одну запись
    def has_add_permission(self, request):
        if ContactPage.objects.exists():
            return False
        return super().has_add_permission(request)