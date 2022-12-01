from typing import List

from django.db import models
from taggit.models import TagBase
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.settings.models import BaseSetting
from wagtail.contrib.settings.registry import register_setting
from wagtail.core.models import Page
from wagtail.documents.models import Document

from mangmap.models.utils import FreeBodyField, SIMPLE_RICH_TEXT_FIELD_FEATURE


class BannerImagePage(Page):
    class Meta:
        abstract = True
    
    banner_image = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name="Bandeau",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = Page.content_panels + [
        FieldPanel("banner_image"),
    ]
    


class ContentPage(BannerImagePage, FreeBodyField):
    class Meta:
        verbose_name = "Page de contenu"
        verbose_name_plural = "Pages de contenu"

    subpage_types: List[str] = ["ContentPage"]

    content_panels = BannerImagePage.content_panels + FreeBodyField.panels


class SiteType(TagBase):
    class Meta:
        ordering = ("name",)
        verbose_name = "Type de site"
        verbose_name_plural = "Types de site"


class ActualityType(TagBase):
    class Meta:
        ordering = ("name",)
        verbose_name = "Type d'actualité"
        verbose_name_plural = "Types d'actualité"


class Thematic(TagBase):
    class Meta:
        verbose_name = "Thématique"
        verbose_name_plural = "Thématiques"

    icon = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def icon_or_default(self):
        if self.icon:
            return self.icon.url
        else:
            return f"/static/img/thematics/{self.slug}.svg"

    def to_dict(self):
        to_return = {"name": self.name, "slug": self.slug, "icon": self.icon_or_default}

        return to_return


@register_setting
class StructureSettings(BaseSetting):
    plateformUrl = models.URLField(
        verbose_name="Lien de la plateforme",
        max_length=300,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Paramètre de la structure"


@register_setting
class AnalyticsScriptSetting(BaseSetting):
    script = models.TextField(
        help_text="Script d'analytics",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Script de suivi du traffic"


@register_setting
class NewsLetterSettings(BaseSetting):
    newsLetter = models.URLField(
        help_text="Lien d'inscription à la lettre d'information",
        max_length=300,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Inscription à la lettre d'information"


class Contact(models.Model):
    firstname = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    subject = models.CharField(max_length=40)
    message = models.TextField()
