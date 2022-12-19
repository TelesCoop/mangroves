import datetime
from django.db import models
from django.utils import translation
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.core.fields import RichTextField
from mangmap.models.models import BannerImagePage, CustomImage
from mangmap.constants import YEAR_Of_CREATION


class HomePage(BannerImagePage, models.Model):
    from mangmap.models.utils import SIMPLE_RICH_TEXT_FIELD_FEATURE

    def get_context(self, request, *args, **kwargs):
        from mangmap.models.site import Site
        from mangmap.models.news import News

        current_language = translation.get_language()

        context = super().get_context(request, *args, **kwargs)
        sites = Site.objects.filter(locale__language_code=current_language)
        news = News.objects.filter(locale__language_code=current_language)
        context["n_sites"] = sites.count()
        context["n_tiles"] = sites.aggregate(n_tiles=models.Sum("tiles_nb"))["n_tiles"]
        context[
            "disponibility_years"
        ] = f"{YEAR_Of_CREATION} - {datetime.date.today().year}"
        first_news = news.filter(is_mangmap=True).first()
        if not first_news:
            first_news = news.first()
        if first_news:
            news_list = [first_news] + list(news.exclude(id=first_news.id)[:2])
        else:
            news_list = news[:3]
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
        CustomImage,
        verbose_name="Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    key_figures_introduction = RichTextField(
        features=SIMPLE_RICH_TEXT_FIELD_FEATURE + ["h2", "h3", "h4", "ol", "ul"],
        verbose_name="Introduction",
        default="Quelques chiffres clés",
    )
    key_figures_sites_nb_title = models.CharField(
        blank=True,
        verbose_name="Titre pour le nombre de site mangroves",
        max_length=64,
        default="Nombre de sites",
    )
    key_figures_tiles_nb_title = models.CharField(
        blank=True,
        verbose_name="Titre pour le nombre de tuiles",
        max_length=64,
        default="Nombre de tuiles",
    )
    key_figures_year = models.CharField(
        blank=True,
        verbose_name="Titre pour les années disponibles",
        max_length=64,
        default="Années disponibles",
    )

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
                FieldPanel("key_figures_introduction"),
                FieldPanel("key_figures_sites_nb_title"),
                FieldPanel("key_figures_tiles_nb_title"),
                FieldPanel("key_figures_year"),
            ],
            heading="Bloc des chiffres clés",
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
