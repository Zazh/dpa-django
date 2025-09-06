from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q, CheckConstraint
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.templatetags.static import static

class Menu(models.Model):
    slug = models.SlugField(_("Slug"), unique=True)          # например: main / footer / sidebar
    title = models.CharField(_("Title"), max_length=200, blank=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Menu")
        verbose_name_plural = _("Menus")

    def __str__(self):
        return self.title or self.slug


class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="items")
    # подпись в меню (переводимая)
    title = models.CharField(_("Title"), max_length=200)

    # куда ведёт пункт: ЛИБО по имени url, ЛИБО абсолютный/относительный путь
    url_name = models.CharField(_("URL name (reverse)"), max_length=200, blank=True,
                                help_text=_("Django URL name, e.g. 'home'"))
    url_path = models.CharField(_("Path or absolute URL"), max_length=500, blank=True,
                                help_text=_("'/about/' or 'https://example.com'"))

    # поведение
    open_in_new_tab = models.BooleanField(_("Open in new tab"), default=False)
    visible = models.BooleanField(_("Visible"), default=True)

    # сортировка
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("Menu item")
        verbose_name_plural = _("Menu items")

    def __str__(self):
        return f"{self.menu}: {self.title}"

class HomePage(models.Model):
    hero_title = models.CharField(_("Hero title"), max_length=200)
    hero_subtitle = models.CharField(_("Hero subtitle"), max_length=300, blank=True)
    mission_text = models.CharField(_("Mission text"), max_length=300, blank=True)
    education_title = models.CharField(_("Education title"), max_length=300, blank=True)
    meta_title = models.CharField(_("Meta title"), max_length=255, blank=True)
    meta_description = models.TextField(_("Meta description"), blank=True)

    class Meta:
        verbose_name = _("Home page")
        verbose_name_plural = _("Home pages")

    def __str__(self):
        return self.meta_title or "Home"


class AboutPage(models.Model):
    title = models.CharField(_("Title"), max_length=200, blank=True)
    subtitle = models.TextField(_("Subtitle"), blank=True)
    education_title = models.CharField(_("Education title"), max_length=300, blank=True)
    mission_text = models.CharField(_("Mission text"), max_length=300, blank=True)

    meta_title = models.CharField(_("Meta title"), max_length=255, blank=True)
    meta_description = models.TextField(_("Meta description"), blank=True)

    class Meta:
        verbose_name = _("About page")
        verbose_name_plural = _("About pages")

    def __str__(self):
        return self.meta_title or "About"


class BenefitSection(models.Model):
    slug = models.SlugField(_("Slug"), blank=True,
                            help_text=_("Уникальный идентификатор секции для шаблона"))
    title = models.CharField(_("Title"), max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("Benefit section")
        verbose_name_plural = _("Benefit sections")

    def __str__(self):
        return self.title or self.slug


class BenefitItem(models.Model):
    section = models.ForeignKey(BenefitSection, on_delete=models.CASCADE, related_name="items")
    label = models.CharField(_("Label"), max_length=120, blank=True)
    detail = models.CharField(_("Detail"), max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("Benefit item")
        verbose_name_plural = _("Benefit items")

    def __str__(self):
        return self.label or f"Benefit item #{self.pk}"


# team
class TeamBlock(models.Model):
    slug = models.SlugField(_("Slug"), unique=True, default="team-core")
    title = models.CharField(_("Title"), max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("Team block")
        verbose_name_plural = _("Team blocks")

    def __str__(self):
        return self.title or self.slug


class TeamMember(models.Model):
    block = models.ForeignKey(TeamBlock, on_delete=models.CASCADE, related_name="members")
    name = models.CharField(_("Name"), max_length=160)
    post = models.CharField(_("Position"), max_length=160, blank=True)
    description = models.TextField(_("Description"), blank=True)
    photo = models.ImageField(_("Photo"), upload_to="team/", blank=True)  # ← ImageField
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("Team member")
        verbose_name_plural = _("Team members")

    def __str__(self):
        return self.name

    # удобный фолбэк, чтобы в шаблоне не писать if/else
    def photo_src(self):
        if self.photo and hasattr(self.photo, "url"):
            return self.photo.url
        return static("dist/images/team-avatar.jpg")


class TeamBlockPlacement(models.Model):
    block = models.ForeignKey(TeamBlock, on_delete=models.CASCADE, related_name="placements")

    page_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    page_object_id = models.PositiveIntegerField()
    page = GenericForeignKey("page_content_type", "page_object_id")

    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        unique_together = (("block", "page_content_type", "page_object_id"),)
        verbose_name = _("Team block placement")
        verbose_name_plural = _("Team block placements")

    def __str__(self):
        return f"{self.block} → {self.page}"


# --- Partners
class PartnersBlock(models.Model):
    slug = models.SlugField(_("Slug"), unique=True, default="partners-core")
    title = models.CharField(_("Title"), max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("Partners block")
        verbose_name_plural = _("Partners blocks")

    def __str__(self):
        return self.title or self.slug


class PartnerLogo(models.Model):
    block = models.ForeignKey(PartnersBlock, on_delete=models.CASCADE, related_name="logos")
    svg_code = models.TextField(_("Inline SVG"))
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("Partner logo")
        verbose_name_plural = _("Partner logos")

    def __str__(self):
        return f"Logo #{self.pk} of {self.block}"


class PartnersBlockPlacement(models.Model):
    block = models.ForeignKey(PartnersBlock, on_delete=models.CASCADE, related_name="placements")

    page_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    page_object_id = models.PositiveIntegerField()
    page = GenericForeignKey("page_content_type", "page_object_id")

    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        unique_together = (("block", "page_content_type", "page_object_id"),)
        verbose_name = _("Partners block placement")
        verbose_name_plural = _("Partners block placements")

    def __str__(self):
        return f"{self.block} → {self.page}"


# ---- Gallery Block ----
class GalleryBlock(models.Model):
    slug = models.SlugField(_("Slug"), unique=True, default="core-gallery")
    title = models.CharField(_("Title"), max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("Gallery block")
        verbose_name_plural = _("Gallery blocks")

    def __str__(self):
        return self.title or self.slug


class GalleryItem(models.Model):
    block = models.ForeignKey(GalleryBlock, on_delete=models.CASCADE, related_name="items")
    image = models.ImageField(_("Image"), upload_to="gallery/")
    alt = models.CharField(_("Alt text"), max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("Gallery item")
        verbose_name_plural = _("Gallery items")

    def __str__(self):
        return self.alt or f"Item #{self.pk}"


class GalleryBlockPlacement(models.Model):
    block = models.ForeignKey(GalleryBlock, on_delete=models.CASCADE, related_name="placements")
    page_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    page_object_id = models.PositiveIntegerField()
    page = GenericForeignKey("page_content_type", "page_object_id")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        unique_together = (("block", "page_content_type", "page_object_id"),)
        verbose_name = _("Gallery block placement")
        verbose_name_plural = _("Gallery block placements")

    def __str__(self):
        return f"{self.block} → {self.page}"


# --- Social link ----
class SocialLinksBlock(models.Model):
    slug = models.SlugField(_("Slug"), unique=True, default="social-core")
    title = models.CharField(_("Title"), max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("Social links block")
        verbose_name_plural = _("Social links blocks")

    def __str__(self):
        return self.title or self.slug


class SocialLinkItem(models.Model):
    block = models.ForeignKey(SocialLinksBlock, on_delete=models.CASCADE, related_name="items")
    label = models.CharField(_("Accessible label / tooltip"), max_length=120, blank=True)
    url = models.URLField(_("URL"), max_length=500)
    svg_code = models.TextField(_("Inline SVG"))  # вставляешь <svg ...>...</svg>
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("Social link")
        verbose_name_plural = _("Social links")

    def __str__(self):
        return self.label or self.url


class SocialLinksBlockPlacement(models.Model):
    block = models.ForeignKey(SocialLinksBlock, on_delete=models.CASCADE, related_name="placements")

    page_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    page_object_id = models.PositiveIntegerField()
    page = GenericForeignKey("page_content_type", "page_object_id")

    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        unique_together = (("block", "page_content_type", "page_object_id"),)
        verbose_name = _("Social links block placement")
        verbose_name_plural = _("Social links block placements")

    def __str__(self):
        return f"{self.block} → {self.page}"


# ---- Services -----
class ServicePage(models.Model):
    slug = models.SlugField(_("Slug"), unique=True)
    title = models.CharField(_("Офер"), max_length=200)
    subtitle = models.TextField(_("УТП"), blank=True)

    program_title = models.CharField(_("Program title"), max_length=200, blank=True, default="Program")

    # флаги/порядок для карточек
    show = models.BooleanField(_("Show in cards"), default=True, db_index=True)
    services_order = models.PositiveIntegerField(default=0, db_index=True)

    # поля карточки
    card_icon_svg = models.TextField(_("Card icon SVG"), blank=True)
    card_tags_text = models.CharField(_("Card tags (comma-separated)"), max_length=300, blank=True)
    card_title_text = models.CharField(_("Card title"), max_length=300, blank=True)
    card_description_text = models.CharField(_("Card description"), max_length=300, blank=True)

    # SEO
    meta_title = models.CharField(_("Meta title"), max_length=255, blank=True)
    meta_description = models.TextField(_("Meta description"), blank=True)

    cta_title = models.CharField(_("CTA title"), max_length=300, blank=True)
    cta_descr = models.CharField(_("CTA descr"), max_length=300, blank=True)


    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Service page")
        verbose_name_plural = _("Service pages")
        ordering = ["services_order", "id"]

    def __str__(self):
        return self.title or self.slug

    def get_absolute_url(self):
        return reverse("service_detail", kwargs={"slug": self.slug})

    @property
    def card_tags(self):
        return [t.strip() for t in (self.card_tags_text or "").split(",") if t.strip()]



class ServiceSlide(models.Model):
    page = models.ForeignKey(ServicePage, on_delete=models.CASCADE, related_name="slides")
    image = models.ImageField(_("Image"), upload_to="services/slides/")
    alt = models.CharField(_("Alt text"), max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("Service slide")
        verbose_name_plural = _("Service slides")

    def __str__(self):
        return self.alt or f"Slide #{self.pk}"

    def image_url(self):
        return self.image.url if self.image and hasattr(self.image, "url") else static("dist/images/cover.jpg")


class ServiceBenefit(models.Model):
    page = models.ForeignKey(ServicePage, on_delete=models.CASCADE, related_name="benefits")
    name = models.CharField(_("Name"), max_length=160)
    value = models.CharField(_("Value"), max_length=160)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("Service benefit")
        verbose_name_plural = _("Service benefits")

    def __str__(self):
        return f"{self.name}: {self.value}"


class ServiceAdvantage(models.Model):
    page = models.ForeignKey(ServicePage, on_delete=models.CASCADE, related_name="advantages")
    icon_svg = models.TextField(_("Inline SVG"), blank=True)
    text = models.TextField(_("Text"), blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("Service advantage")
        verbose_name_plural = _("Service advantages")

    def __str__(self):
        return (self.text[:40] + "…") if self.text else f"Advantage #{self.pk}"


class ServiceProgramItem(models.Model):
    page = models.ForeignKey(ServicePage, on_delete=models.CASCADE, related_name="program_items")
    anchor = models.SlugField(_("Anchor (ID)"), max_length=64, blank=True,
                              help_text=_("Если пусто — сгенерируется автоматически вида program-<id>"))

    title = models.CharField(_("Title"), max_length=200)
    time = models.CharField(_("Duration / time"), max_length=120, blank=True)
    subtitle = models.CharField(_("Subtitle"), max_length=300, blank=True)

    image1 = models.ImageField(_("Image1"), upload_to="program/", blank=True)
    image2 = models.ImageField(_("Image2"), upload_to="program/", blank=True)
    image3 = models.ImageField(_("Image3"), upload_to="program/", blank=True)

    list_text = models.TextField(_("Bullets (one per line)"), blank=True,
                                 help_text=_("Каждый пункт с новой строки."))
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("Program item")
        verbose_name_plural = _("Program items")

    def __str__(self):
        return self.title

    @property
    def bullets(self):
        return [l.strip() for l in (self.list_text or "").splitlines() if l.strip()]

    @property
    def anchor_id(self):
        return self.anchor or f"program-{self.pk}"

    @property
    def images(self):
        """Удобно итерироваться в шаблоне: вернёт список непустых ImageFieldFile."""
        imgs = [self.image1, self.image2, self.image3]
        return [img for img in imgs if getattr(img, "name", "")]


# --- Fleet (авиапарк) ---
class FleetBlock(models.Model):
    slug = models.SlugField(_("Slug"), unique=True, default="fleet-core")
    title = models.CharField(_("Title"), max_length=200, blank=True, default="")
    character_label = models.CharField(_("Character Label"), max_length=100, blank=True, default="Характеристики")
    order = models.PositiveIntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("Fleet block")
        verbose_name_plural = _("Fleet blocks")

    def __str__(self):
        return self.title or self.slug


class FleetItem(models.Model):
    block = models.ForeignKey(FleetBlock, on_delete=models.CASCADE, related_name="items")
    name = models.CharField(_("Name"), max_length=200)
    subtitle = models.CharField(_("Subtitle"), max_length=300, blank=True, default="")
    description = models.TextField(_("Description"), blank=True, default="")
    image = models.ImageField(_("Image"), upload_to="fleet/", blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("Fleet item")
        verbose_name_plural = _("Fleet items")

    def __str__(self):
        return self.name

    @property
    def image_src(self):
        if self.image and hasattr(self.image, "url"):
            return self.image.url
        return static("dist/images/gallery.jpg")  # фолбэк


class FleetSpec(models.Model):
    item = models.ForeignKey(FleetItem, on_delete=models.CASCADE, related_name="specs")
    key = models.CharField(_("Key"), max_length=160)
    value = models.CharField(_("Value"), max_length=200, blank=True, default="")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("Fleet spec")
        verbose_name_plural = _("Fleet specs")

    def __str__(self):
        return f"{self.key}: {self.value}"


# --- FAQ ----
class FaqBlock(models.Model):
    slug    = models.SlugField(_("Slug"), unique=True, default="faq-core")
    title   = models.CharField(_("Title"), max_length=200, blank=True)
    order   = models.PositiveIntegerField(default=0)
    cta_faq = models.CharField(_("Cta faq"), max_length=200, blank=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("FAQ block")
        verbose_name_plural = _("FAQ blocks")

    def __str__(self):
        return self.title or self.slug


class FaqItem(models.Model):
    block    = models.ForeignKey(FaqBlock, on_delete=models.CASCADE, related_name="items")
    question = models.CharField(_("Question"), max_length=300)
    answer   = models.TextField(_("Answer"), blank=True)
    order    = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("FAQ item")
        verbose_name_plural = _("FAQ items")

    def __str__(self):
        return self.question

class ContactPage(models.Model):
    # Заголовок страницы
    title = models.CharField(_("Title"), max_length=200, blank=True)
    subtitle = models.TextField(_("Subtitle"), blank=True)

    # Телефон
    phone_label = models.CharField(_("Phone label"), max_length=120, blank=True, default="")
    phone_number = models.CharField(_("Phone number"), max_length=64, blank=True, default="")

    # Почта
    email_label = models.CharField(_("Email label"), max_length=120, blank=True, default="")
    email = models.EmailField(_("Email"), blank=True)

    # Адрес
    address_label = models.CharField(_("Address label"), max_length=120, blank=True, default="")
    address_text = models.CharField(_("Address text"), max_length=300, blank=True, default="")
    address_url = models.URLField(_("Address URL (map)"), max_length=500, blank=True)

    footer_text = models.TextField(_("Footer text"), blank=True, default="")

    meta_title = models.CharField(_("Meta title"), max_length=255, blank=True)
    meta_description = models.TextField(_("Meta description"), blank=True)

    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Contact page")
        verbose_name_plural = _("Contact pages")

    def __str__(self):
        return self.title or "Contacts"