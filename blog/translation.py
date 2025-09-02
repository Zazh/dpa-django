from modeltranslation.translator import register, TranslationOptions
from .models import BlogPost

@register(BlogPost)
class BlogPostTR(TranslationOptions):
    fields = (
        "title", "subtitle",
        "body_md",
        "meta_title", "meta_description",
        # при желании можно добавить tags_text, если теги тоже переводимые
    )
