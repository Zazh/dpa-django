from django.urls import path
from .views import feedback_submit

urlpatterns = [
    path("submit/", feedback_submit, name="feedback_submit"),
]
