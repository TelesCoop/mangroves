import datetime
from functools import cached_property

from django import forms
from django.db import models
from django.forms import model_to_dict
from django.utils.text import slugify
from django.utils import translation
from wagtail.admin.panels import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import TranslatableMixin, Locale
from wagtail.images.views.serve import generate_image_url
from wagtail.search import index

from mangmap.models.country import Country, WorldZone
from mangmap.models.models import CustomImage, ActualityType
from mangmap.models.site import Site
from mangmap.models.utils import TimeStampedModel, FreeBodyField, LocalizedSelectPanel
from mangmap.templatetags.main_tags import news_page_url


class News(TranslatableMixin, index.Indexed, TimeStampedModel, FreeBodyField):
    name = models.CharField(verbose_name="nom", max_length=255)
    publication_date = models.DateTimeField(
        verbose_name="Date de publication",
        default=datetime.datetime.now,
        help_text="Permet de trier l'ordre d'affichage \
            dans la page des actualités",
    )
    slug = models.SlugField(
        max_length=100,
        verbose_name="Slug (URL de l'actualité)",
        blank=True,
        default="",
        help_text="ce champ est rempli automatiquement s'il est laissé vide",
    )
    introduction = RichTextField(max_length=250)
    image = models.ForeignKey(
        CustomImage,
        verbose_name="Miniature",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    is_mangmap = models.BooleanField(
        verbose_name="Est une nouvelle mangmap",
        help_text="La première actualité mise en avant sur la \
            page d'accueil est la dernière actualité mangmap",
        default=False,
    )
    types = models.ManyToManyField(
        ActualityType,
        blank=True,
        verbose_name="Type",
        related_name="news",
        help_text="Permet le filtrage des actualités",
    )
    is_global = models.BooleanField(
        verbose_name="Concerne tous les pays", default=False
    )
    countries = models.ManyToManyField(
        Country,
        verbose_name="Pays liés",
        blank=True,
        help_text="Ce champ n'est pas encore utilisé",
    )
    zones = models.ManyToManyField(
        WorldZone,
        blank=True,
        verbose_name="Zones du monde liées",
        help_text="Ce champ n'est pas encore utilisé",
    )
    sites = models.ManyToManyField(Site, blank=True, verbose_name="Sites concernés")

    search_fields = [
        index.SearchField("name", partial_match=True),
        index.FilterField("publication_date"),
    ]

    panels = [
        FieldPanel("name"),
        FieldPanel("slug", classname="full"),
        FieldPanel("publication_date"),
        FieldPanel("image"),
        FieldPanel("introduction"),
        FieldPanel("is_mangmap"),
        FieldPanel("body"),
        FieldPanel("types", widget=forms.CheckboxSelectMultiple),
        LocalizedSelectPanel("sites", widget=forms.SelectMultiple),
        FieldPanel("is_global"),
        LocalizedSelectPanel("zones", widget=forms.CheckboxSelectMultiple),
        LocalizedSelectPanel("countries", widget=forms.SelectMultiple),
    ]

    def __str__(self):
        return self.name

    @cached_property
    def original(self):
        french = Locale.objects.get(language_code="fr")
        try:
            return self.get_translation(french)
        except News.DoesNotExist:
            # If the news has never been publish
            # and we previsualize the get_translation return a DoesNotExist
            return self

    @property
    def original_image(self):
        return self.original.image

    @property
    def translated_countries(self):
        language = Locale.objects.get(language_code=translation.get_language())
        if language.language_code == "fr":
            return self.countries.all()
        countries_list = []
        for country in self.original.countries.all():
            try:
                countries_list.append(country.get_translation(language))
            except Country.DoesNotExist:
                countries_list.append(country)
        return countries_list

    @property
    def translated_types(self):
        language = Locale.objects.get(language_code=translation.get_language())
        if language.language_code == "fr":
            return self.types.all()
        types_list = []
        for type in self.original.types.all():
            try:
                types_list.append(type.get_translation(language))
            except ActualityType.DoesNotExist:
                types_list.append(type)
        return types_list

    @property
    def translated_sites(self):
        language = Locale.objects.get(language_code=translation.get_language())
        if language.language_code == "fr":
            return self.sites.all()
        sites_list = []
        for site in self.original.sites.all():
            try:
                sites_list.append(site.get_translation(language))
            except Site.DoesNotExist:
                sites_list.append(site)
        return sites_list

    @property
    def link(self):
        return news_page_url(news=self)

    def to_dict(self, include_linked=True):
        to_return = model_to_dict(
            self,
            fields=[
                "id",
                "name",
                "publication_date",
                "slug",
            ],
        )
        to_return["publication_date"] = self.publication_date.strftime("%d %B %Y")
        to_return["types"] = [type_.slug for type_ in self.translated_types]
        if self.original_image:
            to_return["image_link"] = generate_image_url(
                self.original_image, "fill-432x220"
            )
        else:
            to_return["image_link"] = None
        to_return["introduction"] = str(self.introduction)
        to_return["link"] = self.link

        if include_linked:
            # without this check, there could be an infinite loop in linked news
            to_return["sites"] = [site.to_dict() for site in self.translated_sites]

        return to_return

    # def add_countries_from_zone(self):
    #     # add all countries of all selected zones
    #     for zone in self.zones.all():
    #         for country in zone.country_set.all():
    #             self.countries.add(country)
    #     super().save()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta(TranslatableMixin.Meta):
        verbose_name = "Actualité"
        verbose_name_plural = "Actualités"
        ordering = ["-publication_date"]
