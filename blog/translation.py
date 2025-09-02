# blog/translation.py
from modeltranslation.translator import register, TranslationOptions
from .models import BlogSettings, BlogPost

@register(BlogSettings)
class BlogSettingsTR(TranslationOptions):
    fields = ("title", "meta_title", "meta_description", "meta_keywords")

@register(BlogPost)
class BlogPostTR(TranslationOptions):
    fields = ("title", "subtitle", "body_md", "meta_title", "meta_description")
