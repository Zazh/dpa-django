from modeltranslation.translator import register, TranslationOptions
from .models import HomePage, AboutPage, BenefitSection, BenefitItem, TeamBlock, TeamMember, \
    PartnersBlock, GalleryBlock, GalleryItem, SocialLinksBlock, SocialLinkItem, Menu, MenuItem, ServicePage, \
    ServiceBenefit, ServiceAdvantage, ServiceProgramItem, FleetBlock, FleetItem, FleetSpec, FaqBlock, \
    FaqItem, ContactPage


@register(HomePage)
class HomePageTR(TranslationOptions):
    fields = ("hero_title", "hero_subtitle", "mission_text", "meta_title", "meta_description", "education_title")


@register(AboutPage)
class AboutPageTR(TranslationOptions):
    fields = ("title", "meta_title", "subtitle", "meta_description", "mission_text", "education_title")


@register(BenefitSection)
class BenefitSectionTR(TranslationOptions):
    fields = ("title",)


@register(BenefitItem)
class BenefitItemTR(TranslationOptions):
    fields = ("label", "detail")

@register(TeamBlock)
class TeamBlockTR(TranslationOptions):
    fields = ("title",)

@register(TeamMember)
class TeamMemberTR(TranslationOptions):
    fields = ("name", "post", "description")

@register(PartnersBlock)
class PartnersBlockTR(TranslationOptions):
    fields = ("title",)

@register(GalleryBlock)
class GalleryBlockTR(TranslationOptions):
    fields = ("title",)

@register(GalleryItem)
class GalleryItemTR(TranslationOptions):
    fields = ("alt",)

@register(SocialLinksBlock)
class SocialLinksBlockTR(TranslationOptions):
    fields = ("title",)

@register(SocialLinkItem)
class SocialLinkItemTR(TranslationOptions):
    fields = ("label",)

@register(Menu)
class MenuTR(TranslationOptions):
    fields = ("title",)

@register(MenuItem)
class MenuItemTR(TranslationOptions):
    fields = ("title",)


#--- services ----
@register(ServicePage)
class ServicePageTR(TranslationOptions):
    fields = ("title", "subtitle", "meta_title", "meta_description", "program_title", "card_tags_text", "card_title_text", "card_description_text", "cta_title", "cta_descr")

@register(ServiceBenefit)
class ServiceBenefitTR(TranslationOptions):
    fields = ("name", "value")

@register(ServiceAdvantage)
class ServiceAdvantageTR(TranslationOptions):
    fields = ("text",)

@register(ServiceProgramItem)
class ServiceProgramItemTR(TranslationOptions):
    fields = ("title", "subtitle", "list_text")

@register(FleetBlock)
class FleetBlockTR(TranslationOptions):
    fields = ("title", "character_label",)

@register(FleetItem)
class FleetItemTR(TranslationOptions):
    fields = ("name", "subtitle", "description",)

@register(FleetSpec)
class FleetSpecTR(TranslationOptions):
    fields = ("key", "value",)


@register(FaqBlock)
class FaqBlockTR(TranslationOptions):
    fields = ("title", "cta_faq",)

@register(FaqItem)
class FaqItemTR(TranslationOptions):
    fields = ("question", "answer")

@register(ContactPage)
class ContactPageTR(TranslationOptions):
    fields = (
        "title", "subtitle",
        "phone_label",
        "email_label",
        "address_label", "address_text",
        "footer_text",
        "meta_title", "meta_description",
    )
