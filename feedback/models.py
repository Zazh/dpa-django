from django.db import models
from django.utils.translation import gettext_lazy as _

class FeedbackAction(models.Model):
    slug = models.SlugField(_("Slug"), unique=True)

    # видимая подпись на кнопке
    label = models.CharField(_("Button label"), max_length=200, blank=True)

    # тексты модалки
    modal_title   = models.CharField(_("Modal title"), max_length=200, blank=True)
    submit_label  = models.CharField(_("Submit button label"), max_length=120, blank=True)
    name_label    = models.CharField(_("Name label"), max_length=120, blank=True)
    phone_label   = models.CharField(_("Phone label"), max_length=120, blank=True)
    success_message = models.CharField(_("Success message"), max_length=200, blank=True)

    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Feedback action")
        verbose_name_plural = _("Feedback actions")

    def __str__(self):
        return self.slug


class FeedbackSubmission(models.Model):
    action = models.ForeignKey(FeedbackAction, null=True, blank=True,
                               on_delete=models.SET_NULL, related_name="submissions")
    page   = models.CharField(_("Page URL"), max_length=500, blank=True)
    name   = models.CharField(_("Name"), max_length=200)
    phone  = models.CharField(_("Phone"), max_length=100)

    locale = models.CharField(_("Locale"), max_length=10, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created", "id"]
        verbose_name = _("Feedback submission")
        verbose_name_plural = _("Feedback submissions")

    def __str__(self):
        return f"{self.name} • {self.phone} • {self.created:%Y-%m-%d %H:%M}"
