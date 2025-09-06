from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    # НИЧЕГО больше на "" здесь не подключаем!
]

urlpatterns += i18n_patterns(
    path("admin/", admin.site.urls),
    path("", include("contents.urls")),        # ← только здесь
    path("feedback/", include("feedback.urls")),
    path("blog/", include("blog.urls", namespace="blog")),

    prefix_default_language=True,             # ← корень "/" = язык по умолчанию
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
