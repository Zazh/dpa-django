from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.conf import settings
from django.utils import translation
from contents.models import ServicePage
from blog.models import BlogPost


class StaticViewSitemap(Sitemap):
    """Статические страницы сайта"""
    priority = 0.5
    changefreq = 'monthly'
    protocol = 'https'

    def items(self):
        # URL-имена ваших статических страниц из contents/urls.py
        return [
            'home',  # главная страница
            'about',  # страница о нас
            'contacts',  # контакты (не contact!)
            # services - не добавляем, так как отдельной страницы списка услуг нет
            # отдельные услуги будут в ServicesSitemap
        ]

    def location(self, item):
        return reverse(item)

    def get_urls(self, site=None, **kwargs):
        """Генерируем URL для всех языков"""
        urls = []
        for language_code, language_name in settings.LANGUAGES:
            translation.activate(language_code)
            for item in self.items():
                try:
                    loc = self.location(item)
                    url_info = {
                        'item': item,
                        'location': loc,
                        'lastmod': None,
                        'changefreq': self.changefreq,
                        'priority': str(self.priority),
                        'alternates': []
                    }

                    # Добавляем альтернативные языки
                    for alt_lang_code, alt_lang_name in settings.LANGUAGES:
                        translation.activate(alt_lang_code)
                        try:
                            alt_loc = self.location(item)
                            url_info['alternates'].append({
                                'location': alt_loc,
                                'lang_code': alt_lang_code
                            })
                        except:
                            continue

                    urls.append(url_info)
                except:
                    continue

        translation.deactivate()
        return urls


class ServicesSitemap(Sitemap):
    """Sitemap для страниц услуг"""
    changefreq = "monthly"
    priority = 0.8
    protocol = 'https'

    def items(self):
        return ServicePage.objects.filter(show=True)

    def lastmod(self, obj):
        return obj.updated

    def get_urls(self, site=None, **kwargs):
        """Генерируем URL страниц услуг для всех языков"""
        urls = []
        for language_code, language_name in settings.LANGUAGES:
            translation.activate(language_code)
            for item in self.items():
                try:
                    url_info = {
                        'item': item,
                        'location': item.get_absolute_url(),
                        'lastmod': self.lastmod(item),
                        'changefreq': self.changefreq,
                        'priority': str(self.priority),
                        'alternates': []
                    }

                    # Добавляем альтернативные языки
                    for alt_lang_code, alt_lang_name in settings.LANGUAGES:
                        translation.activate(alt_lang_code)
                        try:
                            alt_loc = item.get_absolute_url()
                            url_info['alternates'].append({
                                'location': alt_loc,
                                'lang_code': alt_lang_code
                            })
                        except:
                            continue

                    urls.append(url_info)
                except:
                    continue

        translation.deactivate()
        return urls


class BlogSitemap(Sitemap):
    """Sitemap для постов блога"""
    changefreq = "weekly"
    priority = 0.7
    protocol = 'https'

    def items(self):
        return BlogPost.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated

    def get_urls(self, site=None, **kwargs):
        """Генерируем URL постов блога для всех языков"""
        urls = []
        for language_code, language_name in settings.LANGUAGES:
            translation.activate(language_code)
            for item in self.items():
                try:
                    url_info = {
                        'item': item,
                        'location': item.get_absolute_url(),
                        'lastmod': self.lastmod(item),
                        'changefreq': self.changefreq,
                        'priority': str(self.priority),
                        'alternates': []
                    }

                    # Добавляем альтернативные языки
                    for alt_lang_code, alt_lang_name in settings.LANGUAGES:
                        translation.activate(alt_lang_code)
                        try:
                            alt_loc = item.get_absolute_url()
                            url_info['alternates'].append({
                                'location': alt_loc,
                                'lang_code': alt_lang_code
                            })
                        except:
                            continue

                    urls.append(url_info)
                except:
                    continue

        translation.deactivate()
        return urls