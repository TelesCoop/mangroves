from functools import cached_property
from django import forms
from django.db import models
from django.forms import model_to_dict
from django.utils.text import slugify
from django.utils import translation
from wagtail.admin.panels import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import TranslatableMixin, Locale
from wagtail.search import index

from mangmap.models.country import Country
from mangmap.models.models import Thematic, SiteType
from mangmap.models.utils import (
    TimeStampedModel,
    SIMPLE_RICH_TEXT_FIELD_FEATURE,
    FreeBodyField,
)


class Site(TimeStampedModel, FreeBodyField, TranslatableMixin, index.Indexed):
    countries = models.ManyToManyField(Country, verbose_name="Pays", blank=True)
    name = models.CharField(verbose_name="Nom", max_length=100)
    slug = models.SlugField(
        max_length=100,
        verbose_name="Slug (URL du site)",
        blank=True,
        default="",
        help_text="ce champ est rempli automatiquement s'il est laissé vide",
    )
    thematics = models.ManyToManyField(
        Thematic, blank=True, verbose_name="Thématiques", related_name="sites"
    )
    main_thematic = models.ForeignKey(
        Thematic,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Thématique principale",
        help_text="ce champ n'est utilisé que lorsque plusieurs thématiques sont sélectionnées",
    )
    source_link = models.CharField(
        verbose_name="Lien vers la Site (URL)", max_length=200, blank=True
    )
    file = models.FileField(
        verbose_name="Fichier source",
        blank=True,
        null=True,
        help_text="S'il est défini, le lien vers la source est ignoré",
    )
    short_description = RichTextField(
        null=True,
        blank=True,
        features=SIMPLE_RICH_TEXT_FIELD_FEATURE,
        verbose_name="Description courte",
        max_length=1000,
    )
    types = models.ManyToManyField(SiteType, blank=True)
    tiles_nb = models.IntegerField(default=0, verbose_name="Nombre de tuiles")
    coastline_coverage = models.CharField(
        verbose_name="Couverture du littoral", max_length=8, blank=True
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
        FieldPanel("short_description"),
        FieldPanel("tiles_nb"),
        FieldPanel("coastline_coverage"),
        FieldPanel("source_link"),
        FieldPanel("file"),
        FieldPanel("body"),
        FieldPanel("countries", widget=forms.CheckboxSelectMultiple),
        FieldPanel("types", widget=forms.CheckboxSelectMultiple),
        FieldPanel("thematics", widget=forms.CheckboxSelectMultiple),
    ]

    def to_dict(self):
        to_return = model_to_dict(
            self,
            fields=[
                "id",
                "name",
                "slug",
                "thematics",
                "short_description",
                "tiles_nb",
                "coastline_coverage",
            ],
        )
        to_return["thematics"] = [
            thematic.slug for thematic in self.translated_thematics
        ]
        to_return["is_description_long"] = (
            is_description_long := len(self.short_description) >= 250
        )
        to_return["short_description_max_250"] = self.short_description[:250]
        if is_description_long:
            to_return["short_description_max_250"] += "..."
        if len(to_return["thematics"]) == 1:
            to_return["thematic"] = to_return["thematics"][0]
        elif len(to_return["thematics"]) > 1 and self.main_thematic:
            to_return["thematic"] = self.main_thematic.slug
        else:
            to_return["thematic"] = "multiple"
        zones = {
            country.zone.code for country in self.translated_countries if country.zone
        }
        if len(zones) == 1:
            to_return["zone"] = next(iter(zones))
        else:
            to_return["zone"] = None
        to_return["link"] = self.link
        if self.file:
            to_return["download_name"] = self.file.name
        else:
            to_return["download_name"] = None
        to_return["is_download"] = self.is_download
        to_return["countries"] = [country.code for country in self.translated_countries]
        to_return["types"] = [type_.slug for type_ in self.translated_types]
        return to_return

    def __str__(self):
        return self.name

    def get_main_thematic(self):
        if self.main_thematic:
            return self.main_thematic
        if self.thematics.count() == 1:
            return self.thematics.first()
        return None

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @cached_property
    def original(self):
        french = Locale.objects.get(language_code="fr")
        try:
            return self.get_translation(french)
        except Site.DoesNotExist:
            # If the site has never been publish
            # and we previsualize the get_translation return a DoesNotExist
            return self

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
    def translated_thematics(self):
        language = Locale.objects.get(language_code=translation.get_language())
        if language.language_code == "fr":
            return self.thematics.all()
        thematics_list = []
        for thematic in self.original.thematics.all():
            try:
                thematics_list.append(thematic.get_translation(language))
            except Thematic.DoesNotExist:
                thematics_list.append(thematic)
        return thematics_list

    @property
    def translated_types(self):
        language = Locale.objects.get(language_code=translation.get_language())
        if language.language_code == "fr":
            return self.types.all()
        types_list = []
        for type in self.original.types.all():
            try:
                types_list.append(type.get_translation(language))
            except SiteType.DoesNotExist:
                types_list.append(type)
        return types_list

    @property
    def link(self):
        if self.file:
            return self.file.url
        if self.source_link:
            return self.source_link

    @property
    def is_download(self):
        return bool(self.file)

    class Meta(TranslatableMixin.Meta):
        verbose_name_plural = "Sites"
        verbose_name = "Site"
        ordering = ("name",)
