from django.views.generic import ListView, DetailView
from django.utils import timezone
from .models import BlogPost

class BlogListView(ListView):
    model = BlogPost
    template_name = "blog/blog.html"
    context_object_name = "posts"
    paginate_by = 9

    def get_queryset(self):
        qs = (BlogPost.objects
              .filter(is_published=True, published_at__lte=timezone.now())
              .only("id", "slug", "title", "subtitle", "image", "published_at", "tags_text")
              .order_by("-published_at", "-id"))
        return qs

class BlogDetailView(DetailView):
    model = BlogPost
    template_name = "blog/blog_detail.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True)
