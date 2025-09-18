from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve as static_serve
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),

    re_path(r"^robots\.txt$",  static_serve, {"path": "robots.txt", "document_root": settings.STATIC_ROOT}),
    re_path(r"^llm\.txt$",     static_serve, {"path": "llm.txt",    "document_root": settings.STATIC_ROOT}),

    # редиректы с префиксов языка
    re_path(r"^(?:ru|kk|en)/robots\.txt$", RedirectView.as_view(url="/robots.txt", permanent=True)),
    re_path(r"^(?:ru|kk|en)/llm\.txt$",    RedirectView.as_view(url="/llm.txt",    permanent=True)),
]

urlpatterns += i18n_patterns(
    path("admin/", admin.site.urls),
    path("", include("contents.urls")),        # ← только здесь
    path("feedback/", include("feedback.urls")),
    path("blog/", include("blog.urls", namespace="blog")),

    prefix_default_language=True,
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
