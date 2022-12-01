from wagtail.core.models import Page
from wagtail.core.templatetags.wagtailcore_tags import pageurl

from mangmap.models import SitesPage, NewsListPage


def general_context(_):
    try:
        home_page = Page.objects.get(content_type__model="homepage")
    except Page.DoesNotExist:
        home_page = None
    try:
        sites_link = pageurl({}, SitesPage.objects.get())
    except SitesPage.DoesNotExist:
        sites_link = None
    try:
        news_list_link = pageurl({}, NewsListPage.objects.get())
    except NewsListPage.DoesNotExist:
        news_list_link = None
    context = {
        "sites_link": sites_link,
        "news_list_link": news_list_link,
        "home_page": home_page,
    }
    return context
