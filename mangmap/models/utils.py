from django.db import models
from django.core.exceptions import ImproperlyConfigured
from django.forms.models import ModelChoiceIterator
from django.forms.widgets import (
    CheckboxSelectMultiple,
    RadioSelect,
    Select,
    SelectMultiple,
)
from django.utils.translation import gettext_lazy as _

from wagtail.admin.panels import FieldPanel
from wagtail.core import blocks
from wagtail.core.models import Locale
from wagtail.core.fields import StreamField
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock


def paragraph_block(additional_field, required):
    return (
        "paragraph",
        blocks.RichTextBlock(
            label="Contenu",
            features=SIMPLE_RICH_TEXT_FIELD_FEATURE
            + ["h3", "h4", "ol", "ul"]
            + additional_field,
            required=required,
        ),
    )


SIMPLE_RICH_TEXT_FIELD_FEATURE = ["bold", "italic", "link"]
COLOR_CHOICES = (
    ("primary-light", "Bleue"),
    ("secondary-light", "Verte"),
    ("white", "Blanche"),
    ("", "Sans couleur"),
)


def get_orignal(instance):
    french = Locale.objects.get(language_code="fr")
    try:
        return instance.get_translation(french)
    except instance.__class__.DoesNotExist:
        return instance


class FreeBodyField(models.Model):
    color_block = (
        "color",
        blocks.ChoiceBlock(
            label="couleur",
            choices=COLOR_CHOICES,
            default="none",
            help_text="Couleur de fond",
            required=False,
        ),
    )
    image_block = (
        "image",
        ImageChooserBlock(label="Image à côté du paragraphe", required=False),
    )

    body = StreamField(
        [
            # Is h1
            (
                "heading",
                blocks.CharBlock(form_classname="full title", label="Titre de la page"),
            ),
            (
                "section",
                blocks.StructBlock(
                    [
                        paragraph_block(["h2"], True),
                        color_block,
                        image_block,
                        (
                            "id",
                            blocks.CharBlock(
                                required=False,
                                help_text="sert à créer des ancres",
                                max_length=50,
                            ),
                        ),
                        (
                            "position",
                            blocks.ChoiceBlock(
                                choices=[
                                    ("right", "Droite"),
                                    ("left", "Gauche"),
                                ],
                                required=False,
                                help_text="Position de l'image",
                            ),
                        ),
                        (
                            "sub_section",
                            blocks.ListBlock(
                                blocks.StructBlock(
                                    [
                                        (
                                            "without_margin_top",
                                            blocks.BooleanBlock(
                                                label="Retirer la marge du dessus",
                                                default=False,
                                                required=False,
                                            ),
                                        ),
                                        color_block,
                                        paragraph_block(["image"], False),
                                        (
                                            "id",
                                            blocks.CharBlock(
                                                required=False,
                                                help_text="sert à créer des ancres",
                                                max_length=50,
                                            ),
                                        ),
                                        (
                                            "columns",
                                            blocks.ListBlock(
                                                blocks.StructBlock(
                                                    [
                                                        color_block,
                                                        paragraph_block(
                                                            ["image"], False
                                                        ),
                                                    ],
                                                    label="Colonne",
                                                ),
                                                label="Colonnes",
                                            ),
                                        ),
                                    ],
                                    label="Sous section",
                                ),
                                default=[],
                                label="Sous sections",
                            ),
                        ),
                    ],
                    label="Section",
                ),
            ),
            ("image", ImageChooserBlock()),
            ("pdf", DocumentChooserBlock()),
        ],
        blank=True,
        verbose_name="Contenu",
        help_text="Corps de la page",
        use_json_field=True,
    )

    panels = [
        FieldPanel("body", classname="full"),
    ]

    class Meta:
        abstract = True


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created`` and ``modified`` fields.

    """

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateField(auto_now=True)

    class Meta:
        abstract = True


class LocalizedSelectPanel(FieldPanel):
    """
    Customised FieldPanel to filter choices based on locale of page/model being created/edited
    Usage:
    widget_class - optional, override field widget type
                 - should be CheckboxSelectMultiple, RadioSelect, Select or SelectMultiple
    typed_choice_field - set to True with Select widget forces drop down list
    """

    def __init__(
        self, field_name, widget_class=None, typed_choice_field=False, *args, **kwargs
    ):
        if widget_class not in [
            None,
            CheckboxSelectMultiple,
            RadioSelect,
            Select,
            SelectMultiple,
        ]:
            raise ImproperlyConfigured(
                _(
                    "widget_class should be a Django form widget class of type "
                    "CheckboxSelectMultiple, RadioSelect, Select or SelectMultiple"
                )
            )
        self.widget_class = widget_class
        self.typed_choice_field = typed_choice_field
        super().__init__(field_name, *args, **kwargs)

    def clone_kwargs(self):
        return {
            "heading": self.heading,
            "classname": self.classname,
            "help_text": self.help_text,
            "widget_class": self.widget_class,
            "typed_choice_field": self.typed_choice_field,
            "field_name": self.field_name,
        }

    class BoundPanel(FieldPanel.BoundPanel):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            if not self.panel.widget_class:
                self.form.fields[self.field_name].widget.choices = self.choice_list
            else:
                self.form.fields[self.field_name].widget = self.panel.widget_class(
                    choices=self.choice_list
                )
            if self.panel.typed_choice_field:
                self.form.fields[
                    self.field_name
                ].__class__.__name__ = "typed_choice_field"
            pass

        @property
        def choice_list(self):
            self.form.fields[self.field_name].queryset = self.form.fields[
                self.field_name
            ].queryset.filter(locale_id=self.instance.locale_id)
            choices = ModelChoiceIterator(self.form.fields[self.field_name])
            return choices
