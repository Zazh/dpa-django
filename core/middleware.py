from django.conf import settings
from django.utils.translation import activate

class ForceDefaultLanguageOnRootMiddleware:
    """
    На URL без языкового префикса форсируем дефолтный язык (например, 'ru'),
    чтобы кука django_language/Accept-Language не перебивали главную.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.default = (settings.LANGUAGE_CODE.split('-')[0]).lower()
        self.prefixes = {code.lower() for code, _ in settings.LANGUAGES}

    def __call__(self, request):
        path = (request.path_info or '/').lower()

        # Есть ли префикс из LANGUAGES? (/, /ru/, /en/, /kk/ и т.п.)
        has_prefix = any(path == f'/{code}/' or path.startswith(f'/{code}/') for code in self.prefixes)

        if not has_prefix:
            activate(self.default)
            request.LANGUAGE_CODE = self.default

        return self.get_response(request)
