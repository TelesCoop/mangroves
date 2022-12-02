from django.conf import settings
from django.utils import translation
from django.templatetags.static import static

from mangmap.models import HomePage


class SearchDescriptionAndTranslationMiddleware:
    """Middleware to add search_description, seo_title and translated_url to the context."""

    def __init__(self, get_response):
        from wagtail.core.models import Locale

        self.get_response = get_response
        locales = Locale.objects.all()
        language_to_locale_id = {locale.language_code: locale.id for locale in locales}
        self.home_pages = {
            locale.language_code: HomePage.objects.filter(
                locale=language_to_locale_id[locale.language_code]
            ).first()
            for locale in locales
        }

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_template_response(self, request, response):
        context = response.context_data
        current_language = translation.get_language()
        translated_language = [
            language[0]
            for language in settings.LANGUAGES
            if language[0] != current_language
        ][0]
        try:
            translated_home_page = self.home_pages[translated_language]
        except KeyError:
            translated_home_page = self.home_pages[current_language]
        translated_url = translated_home_page and translated_home_page.url

        seo_title = None
        search_description = None
        seo_image = static("img/mangmap/logo_couleur.svg")
        if not context:
            return response
        elif context.get("page"):
            translations = context["page"].get_translations()
            if len(translations):
                page_translation = translations[0]
                if page_translation:
                    translated_url = page_translation.url
                # for pages, seo_title and title are already correctly taken in to
                # account

            seo_title = context["page"].seo_title or context["page"].title
            search_description = context["page"].search_description
            if hasattr(context["page"], "image") and context["page"].image:
                seo_image = context["page"].image.file.url

        # TODO
        # if not search_description:
        #     search_description = getattr(
        #         SeoSettings.for_request(request),
        #         f"search_description_{current_language}",
        #     )

        context["seo_title"] = seo_title
        context["search_description"] = search_description
        context["seo_image"] = settings.WAGTAILADMIN_BASE_URL + seo_image
        context["translated_url"] = translated_url
        return response
