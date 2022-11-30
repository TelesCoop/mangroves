from django.contrib.syndication.views import Feed

from main.models.news import News
from main.templatetags.main_tags import news_page_url


class LatestNewsFeed(Feed):
    title = "News"
    link = "/feed/news/latest"
    description = "Les dernières actualités de mangmap."
    description_template = "rss_feed.html"

    def items(self):
        return News.objects.order_by("-publication_date")[:5]

    def item_title(self, item):
        return item.name

    def item_link(self, item):
        return news_page_url(item)

    def get_context_data(self, **kwargs):
        """
        {'obj': item, 'site': current_site} as the super context.
        """
        context = super().get_context_data(**kwargs)
        context["image_url"] = (
            context["site"].domain + context["obj"].image.file.url
            if context["obj"].image
            else None
        )
        return context
