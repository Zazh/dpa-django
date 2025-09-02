from typing import Any, Dict

from django.conf import settings
from django.db.models import Prefetch
from django.http import Http404
from django.utils.translation import override, get_language_from_path

from django.views.generic import TemplateView, DetailView

from .models import (
    HomePage, AboutPage,
    BenefitSection, BenefitItem,
    ServicePage, ServiceSlide, ServiceBenefit, ServiceAdvantage,
    ServiceProgramItem, ContactPage,
)

class HomePageView(TemplateView):
    template_name = "contents/home.html"


    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        page = HomePage.objects.first()
        if not page:
            raise Http404("HomePage не настроена в админке.")

        items_qs = BenefitItem.objects.order_by("order", "id")
        benefit_section = (
            BenefitSection.objects
            .filter(slug="home-benefits")
            .prefetch_related(Prefetch("items", queryset=items_qs))
            .first()
        )

        ctx.update({
            "page": page,
            "benefit_section": benefit_section,
        })
        return ctx



class AboutPageView(TemplateView):
    template_name = "contents/about.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        page = AboutPage.objects.first()
        if not page:
            raise Http404("AboutPage не настроена в админке.")

        items_qs = BenefitItem.objects.order_by("order", "id")
        benefit_section = (
            BenefitSection.objects
            .filter(slug="about-benefits")
            .prefetch_related(Prefetch("items", queryset=items_qs))
            .first()
        )

        ctx.update({
            "page": page,
            "benefit_section": benefit_section,
        })
        return ctx


class ServiceDetailView(DetailView):
    model = ServicePage
    template_name = "contents/service_detail.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return (
            ServicePage.objects
            .prefetch_related(
                Prefetch("slides", queryset=ServiceSlide.objects.order_by("order", "id")),
                Prefetch("benefits", queryset=ServiceBenefit.objects.order_by("order", "id")),
                Prefetch("advantages", queryset=ServiceAdvantage.objects.order_by("order", "id")),
                Prefetch("program_items", queryset=ServiceProgramItem.objects.order_by("order", "id")),
            )
        )

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        ctx["page"] = self.object
        return ctx

class ContactPageView(TemplateView):
    template_name = "contents/contacts.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        page = ContactPage.objects.first()
        if not page:
            raise Http404("ContactPage не настроена в админке.")
        ctx["page"] = page
        return ctx