from django.contrib.auth.models import User
from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.core.fields import RichTextField
from mangmap.models.models import BannerImagePage


class HomePage(BannerImagePage, models.Model):
    from mangmap.models.utils import SIMPLE_RICH_TEXT_FIELD_FEATURE
    

    def get_context(self, request, *args, **kwargs):
        from mangmap.models.site import Site
        from mangmap.models.news import News

        context = super().get_context(request, *args, **kwargs)
        context["n_sites"] = Site.objects.count()
        context["n_members"] = User.objects.count()
        first_news = News.objects.filter(is_mangmap=True).first()
        if not first_news:
            first_news = News.objects.filter().first()
        if first_news:
            news_list = [first_news] + list(News.objects.exclude(id=first_news.id)[:2])
        else:
            news_list = News.objects.all()[:3]
        context["news_list"] = news_list
        context["newsletter_link"] = "newsletter-link"
        return context

    # HomePage can be created only on the root
    parent_page_types = ["wagtailcore.Page"]

    introduction = RichTextField(
        null=True,
        blank=True,
        features=SIMPLE_RICH_TEXT_FIELD_FEATURE,
        verbose_name="Introduction",
    )
    news_block_title = models.CharField(
        blank=True,
        verbose_name="Titre du bloc des actualités",
        max_length=64,
        default="Dernières actualités",
    )

    content_panels = BannerImagePage.content_panels + [
        FieldPanel("introduction"),
        FieldPanel("news_block_title"),
    ]

    class Meta:
        verbose_name = "Page d'accueil"
