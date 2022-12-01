import json
from typing import List

from django.forms import model_to_dict
from wagtail.contrib.routable_page.models import RoutablePageMixin
from wagtail.core.models import Page

from mangmap.models import Thematic
from mangmap.models.country import Country
from mangmap.models.country import WorldZone
from mangmap.models.models import SiteType
from mangmap.models.site import Site


class SitesPage(RoutablePageMixin, Page):
    class Meta:
        verbose_name = "Page des sites"
        verbose_name_plural = "Pages des sites"

    parent_page_types = ["mangmap.HomePage"]
    subpage_types: List[str] = []
    max_count_per_parent = 1

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["has_vue"] = True

        context["thematics"] = json.dumps(
            [thematic.to_dict() for thematic in Thematic.objects.all()]
        )
        context["site_types"] = json.dumps(
            [model_to_dict(type_) for type_ in SiteType.objects.all()]
        )
        context["zones"] = json.dumps(
            [zone.to_dict() for zone in WorldZone.objects.all()]
        )
        context["sites"] = json.dumps(
            [site.to_dict() for site in Site.objects.all()]
        )
        context["countries"] = json.dumps(
            [country.to_dict() for country in Country.objects.all()]
        )
        return context