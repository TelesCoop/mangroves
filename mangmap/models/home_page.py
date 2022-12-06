from django.contrib.auth.models import User
from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
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

    platform_block_title = models.CharField(
        blank=True,
        verbose_name="Titre",
        max_length=64,
        default="Notre plateforme",
    )
    platform_block_description = RichTextField(
        null=True,
        blank=True,
        features=SIMPLE_RICH_TEXT_FIELD_FEATURE + ["h2", "h3", "h4", "ol", "ul"],
        verbose_name="Description",
    )
    platform_block_cta = models.CharField(
        blank=True,
        verbose_name="Text du bouton",
        max_length=32,
        default="Voir la plateforme",
    )

    platform_block_image = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name="Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    # TODO Chiffres clès 
    
    contact_block_title = models.CharField(
        blank=True,
        verbose_name="Titre",
        max_length=64,
        default="Conactez-nous",
    )
    contact_block_description = models.CharField(
        blank=True,
        verbose_name="Description",
        max_length=256,
    )
    contact_block_cta = models.CharField(
        blank=True,
        verbose_name="Text du bouton",
        max_length=32,
        default="Accéde au formulaire",
    )

    content_panels = BannerImagePage.content_panels + [
        FieldPanel("introduction"),
        FieldPanel("news_block_title"),
        MultiFieldPanel(
            [
                FieldPanel("platform_block_title"),
                FieldPanel("platform_block_description"),
                FieldPanel("platform_block_cta"),
                FieldPanel("platform_block_image"),
            ],
            heading="Bloc concernant la plateforme",
        ),
        MultiFieldPanel(
            [
                FieldPanel("contact_block_title"),
                FieldPanel("contact_block_description"),
                FieldPanel("contact_block_cta"),
            ],
            heading="Bloc Contactez-nous",
        ),
    ]

    class Meta:
        verbose_name = "Page d'accueil"
