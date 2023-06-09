import json
from typing import List

from django.forms import model_to_dict
from django.db import models
from django.utils import translation
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField

from mangmap.models import Thematic
from mangmap.models.country import Country
from mangmap.models.country import WorldZone
from mangmap.models.models import SiteType
from mangmap.models.site import Site


class SitesPage(RoutablePageMixin, Page):
    from mangmap.models.utils import SIMPLE_RICH_TEXT_FIELD_FEATURE

    class Meta:
        verbose_name = "Page des sites"
        verbose_name_plural = "Pages des sites"

    parent_page_types = ["mangmap.HomePage"]
    subpage_types: List[str] = []
    max_count_per_parent = 1

    introduction = RichTextField(
        null=True,
        blank=True,
        features=SIMPLE_RICH_TEXT_FIELD_FEATURE + ["h2", "h3", "h4", "ol", "ul"],
        verbose_name="Introduction",
    )

    list_displayed = models.BooleanField(
        default=True, verbose_name="Affichage de la version en liste"
    )

    content_panels = Page.content_panels + [
        FieldPanel("introduction"),
        FieldPanel("list_displayed"),
    ]

    def get_context(self, request, *args, **kwargs):
        current_language = translation.get_language()

        context = super().get_context(request, *args, **kwargs)
        context["has_vue"] = True

        context["thematics"] = json.dumps(
            [
                thematic.to_dict()
                for thematic in Thematic.objects.filter(
                    locale__language_code=current_language
                )
            ]
        )
        context["site_types"] = json.dumps(
            [
                model_to_dict(type_)
                for type_ in SiteType.objects.filter(
                    locale__language_code=current_language
                )
            ]
        )
        context["zones"] = json.dumps(
            [
                zone.to_dict()
                for zone in WorldZone.objects.filter(
                    locale__language_code=current_language
                )
            ]
        )
        sites = Site.objects.filter(locale__language_code=current_language)
        context["sites"] = json.dumps([site.to_dict() for site in sites])
        context["countries"] = json.dumps(
            [
                country.to_dict()
                for country in Country.objects.filter(
                    locale__language_code=current_language
                )
            ]
        )

        sites_per_zone = {}
        for site in sites:
            sites_per_zone.setdefault(
                site.translated_countries[0].zone.name, []
            ).append(site.to_dict())
        context["sites_per_zone"] = json.dumps(sites_per_zone)

        return context
