from typing import List

from django.forms import model_to_dict
from django.http import Http404
from django.utils import translation
from rest_framework.utils import json
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.models import Page

from mangmap.models import ActualityType
from mangmap.models.news import News


class NewsListPage(RoutablePageMixin, Page):
    class Meta:
        verbose_name = "Page des actualités"
        verbose_name_plural = "Pages des actualités"

    parent_page_types = ["mangmap.HomePage"]
    subpage_types: List[str] = []
    max_count_per_parent = 1

    @route(r"^(.*)/$", name="news")
    def access_news_page(self, request, news_slug):
        try:
            news = News.objects.get(slug=news_slug, locale_id=self.locale_id)
        except (News.DoesNotExist, News.MultipleObjectsReturned):
            raise Http404

        modal_images = []
        for block in news.body:
            if block.block_type == "image":
                modal_images.append(block.value)

        return self.render(
            request,
            context_overrides={
                "news": news,
                "news_page": NewsListPage.objects.filter(
                    locale_id=self.locale_id
                ).first(),
                "modal_images": modal_images,
            },
            template="mangmap/news_page.html",
        )

    def get_context(self, request, *args, **kwargs):
        current_language = translation.get_language()
        context = super().get_context(request, *args, **kwargs)
        context["has_vue"] = True
        context["types"] = json.dumps(
            [
                model_to_dict(type_)
                for type_ in ActualityType.objects.filter(
                    locale__language_code=current_language
                )
            ]
        )
        context["news_list"] = json.dumps(
            [
                news.to_dict()
                for news in News.objects.filter(locale__language_code=current_language)
            ]
        )

        return context
