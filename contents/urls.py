from django.urls import path
from .views import HomePageView, AboutPageView, ServiceDetailView, ContactPageView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("services/<slug:slug>/", ServiceDetailView.as_view(), name="service_detail"),
    path("contacts/", ContactPageView.as_view(), name="contacts"),  # ← страница контактов

]
