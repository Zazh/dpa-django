from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class BlogPost(models.Model):
    slug = models.SlugField(_("Slug"), unique=True)

    title = models.CharField(_("Title"), max_length=200)
    subtitle = models.CharField(_("Subtitle"), max_length=300, blank=True)

    author = models.CharField(_("Author"), max_length=160, blank=True)
    published_at = models.DateTimeField(_("Published at"), default=timezone.now)

    # Теги одной строкой, через запятую
    tags_text = models.CharField(_("Tags (comma-separated)"), max_length=300, blank=True)

    image = models.ImageField(_("Image"), upload_to="blog/", blank=True)

    # Тело в Markdown (дальше отрендерим через фильтр с очисткой)
    body_md = models.TextField(_("Body (Markdown)"), blank=True)

    # SEO (по желанию)
    meta_title = models.CharField(_("Meta title"), max_length=255, blank=True)
    meta_description = models.TextField(_("Meta description"), blank=True)

    # служебное
    is_published = models.BooleanField(_("Published"), default=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at", "-id"]
        verbose_name = _("Blog post")
        verbose_name_plural = _("Blog posts")

    def __str__(self):
        return self.title or self.slug

    @property
    def tags(self):
        return [t.strip() for t in (self.tags_text or "").split(",") if t.strip()]

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"slug": self.slug})
