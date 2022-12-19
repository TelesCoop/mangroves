from typing import List

from django.utils.text import slugify
from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSetting
from wagtail.contrib.settings.registry import register_setting
from wagtail.core.models import Page, TranslatableMixin
from wagtail.documents.models import Document
from wagtail.images.models import Image, AbstractImage, AbstractRendition

from mangmap.models.utils import FreeBodyField


class CustomImage(AbstractImage):
    caption = models.TextField(verbose_name="Légende et/ou Copyright", blank=True)

    admin_form_fields = Image.admin_form_fields + ("caption",)


class CustomRendition(AbstractRendition):
    image = models.ForeignKey(
        CustomImage, on_delete=models.CASCADE, related_name="renditions"
    )

    class Meta:
        unique_together = (("image", "filter_spec", "focal_point_key"),)


class BannerImagePage(Page):
    class Meta:
        abstract = True

    banner_image = models.ForeignKey(
        CustomImage,
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

    show_in_footer = models.BooleanField(
        verbose_name="Faire apparaître dans le bas de page",
        default=False,
        help_text="Si un lien vers cette page devra \
            apparaître dans le bas de page",
    )

    content_panels = BannerImagePage.content_panels + FreeBodyField.panels

    promote_panels = Page.promote_panels + [
        MultiFieldPanel(
            [
                FieldPanel("show_in_footer"),
            ],
            heading="Pour le bas de page du site",
        ),
    ]


class Tag(models.Model):
    name = models.CharField(verbose_name="Nom", max_length=100)
    slug = models.SlugField(
        verbose_name="Slug",
        max_length=100,
        allow_unicode=True,
        blank=True,
        help_text="ce champ est rempli automatiquement s'il est laissé vide",
    )

    def __str__(self):
        return self.name

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class SiteType(TranslatableMixin, Tag):
    class Meta(TranslatableMixin.Meta):
        ordering = ("name",)
        verbose_name = "Type de site"
        verbose_name_plural = "Types de site"


class ActualityType(TranslatableMixin, Tag):
    class Meta(TranslatableMixin.Meta):
        ordering = ("name",)
        verbose_name = "Type d'actualité"
        verbose_name_plural = "Types d'actualité"


class Thematic(TranslatableMixin, Tag):
    class Meta(TranslatableMixin.Meta):
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


class Contact(models.Model):
    firstname = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    subject = models.CharField(max_length=40)
    message = models.TextField()
