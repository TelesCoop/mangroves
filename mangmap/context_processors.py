import datetime
from collections import defaultdict
from typing import Dict, Union
from django.conf import settings
from django.utils import translation
from wagtail.core.templatetags.wagtailcore_tags import pageurl

from mangmap.models import SitesPage, NewsListPage

DEFAULT_LANGUAGE = settings.LANGUAGES[0][0]
LAST_UPDATE: Dict[str, Union[None, datetime.datetime]] = {
    "general_context": None,
}

def is_recent(key: str):
    """Check if values for the given key have been updated recently."""
    if not LAST_UPDATE[key]:
        return False
    return (datetime.datetime.now() - LAST_UPDATE[key]).total_seconds() < 60  # type: ignore


def update_last_change(key):
    """Mark key as last updated now."""
    LAST_UPDATE[key] = datetime.datetime.now()

def load_general_context(_):
    from wagtail.core.models import Page, Locale
    language_to_locale_id = {
        locale.language_code: locale.id for locale in Locale.objects.all()
    }
    context_per_language = defaultdict(dict)
    default_locale_id = language_to_locale_id[DEFAULT_LANGUAGE]

    def get_localized_page(page: Page, language: str) -> Page:
        if language == settings.LANGUAGES[0][0]:
            return page
        locale_id = language_to_locale_id[language]
        return Page.objects.filter(
            translation_key=page.translation_key, locale_id=locale_id
        ).first()


    # Add home page   
    home_page_in_default_language = Page.objects.filter(content_type__model="homepage",
            locale_id=default_locale_id
        ).first()
    for language_code, _ in language_to_locale_id.items():
        if home_page_in_default_language:
            localized_page = get_localized_page(home_page_in_default_language, language_code)
        else:
            localized_page = None
        context_per_language[language_code]["home_page"] = localized_page

    # Add sites_link 
    sites_page_in_default_language = SitesPage.objects.filter(locale_id=default_locale_id).first()
    for language_code, _ in language_to_locale_id.items():
        if sites_page_in_default_language:
            localized_page = get_localized_page(sites_page_in_default_language, language_code)
        else:
            localized_page = None
        context_per_language[language_code]["sites_link"] = pageurl({}, localized_page)
        
    # Add news_list_link 
    news_list_page_in_default_language = NewsListPage.objects.filter(locale_id=default_locale_id).first()
    for language_code, _ in language_to_locale_id.items():
        if news_list_page_in_default_language:
            localized_page = get_localized_page(news_list_page_in_default_language, language_code)
        else:
            localized_page = None
        context_per_language[language_code]["news_list_link"] = pageurl({}, localized_page)

    return context_per_language

def general_context(_):
    if not is_recent("general_context"):
        update_last_change("general_context")
        general_context._general_context = load_general_context(_)
    language = translation.get_language()
    if (
        getattr(general_context, "_general_context")
        and language in general_context._general_context
    ):
        return general_context._general_context[language]
    return {}

def language(_):
    """Templates need a language_code. Will be overriden by django if defined."""
    return {"language_code": translation.get_language()}
