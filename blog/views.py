# blog/views.py
from types import SimpleNamespace
from django.utils.translation import gettext as _
from django.views.generic import ListView, DetailView
from django.utils import timezone
from .models import BlogPost, BlogSettings

class BlogListView(ListView):
    model = BlogPost
    template_name = "blog/blog.html"
    context_object_name = "posts"
    paginate_by = 9

    def get_queryset(self):
        return (
            BlogPost.objects
            .filter(is_published=True, published_at__lte=timezone.now())
            .only("id", "slug", "title", "subtitle", "image", "published_at", "tags_text")
            .order_by("-published_at", "-id")
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        page = BlogSettings.objects.first()
        if not page:
            page = SimpleNamespace(
                title=_("Blog"),
                meta_title=_("Blog"),
                meta_description="",
                meta_keywords="",
            )
        ctx["page"] = page
        return ctx

class BlogDetailView(DetailView):
    model = BlogPost
    template_name = "blog/blog_detail.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True, published_at__lte=timezone.now())
