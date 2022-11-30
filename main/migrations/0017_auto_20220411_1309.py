# Generated by Django 3.2.11 on 2022-04-11 13:09

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.documents.blocks
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailforms", "0004_add_verbose_name_plural"),
        ("wagtailcore", "0066_collection_management_permissions"),
        ("wagtailredirects", "0006_redirect_increase_max_length"),
        ("main", "0016_auto_20220411_1043"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contentpage",
            name="body",
            field=wagtail.core.fields.StreamField(
                [
                    (
                        "heading",
                        wagtail.core.blocks.CharBlock(
                            form_classname="full title", label="Titre de la page"
                        ),
                    ),
                    (
                        "section",
                        wagtail.core.blocks.StructBlock(
                            [
                                (
                                    "color",
                                    wagtail.core.blocks.ChoiceBlock(
                                        choices=[
                                            ("blue", "Bleue"),
                                            ("pink", "Rose"),
                                            ("white", "Blanche"),
                                            ("none", "Sans couleur"),
                                        ],
                                        help_text="Couleur de fond",
                                    ),
                                ),
                                (
                                    "image",
                                    wagtail.images.blocks.ImageChooserBlock(
                                        label="Image à côté du paragraphe",
                                        required=False,
                                    ),
                                ),
                                (
                                    "position",
                                    wagtail.core.blocks.ChoiceBlock(
                                        choices=[
                                            ("right", "Droite"),
                                            ("left", "Gauche"),
                                        ],
                                        help_text="Position de l'image",
                                        required=False,
                                    ),
                                ),
                                (
                                    "paragraph",
                                    wagtail.core.blocks.RichTextBlock(
                                        features=[
                                            "bold",
                                            "italic",
                                            "link",
                                            "h3",
                                            "h4",
                                            "ol",
                                            "ul",
                                            "h2",
                                        ],
                                        label="Contenu",
                                        required=True,
                                    ),
                                ),
                                (
                                    "sub_section",
                                    wagtail.core.blocks.ListBlock(
                                        wagtail.core.blocks.StructBlock(
                                            [
                                                (
                                                    "color",
                                                    wagtail.core.blocks.ChoiceBlock(
                                                        choices=[
                                                            ("blue", "Bleue"),
                                                            ("pink", "Rose"),
                                                            ("white", "Blanche"),
                                                            ("none", "Sans couleur"),
                                                        ],
                                                        help_text="Couleur de fond",
                                                    ),
                                                ),
                                                (
                                                    "paragraph",
                                                    wagtail.core.blocks.RichTextBlock(
                                                        features=[
                                                            "bold",
                                                            "italic",
                                                            "link",
                                                            "h3",
                                                            "h4",
                                                            "ol",
                                                            "ul",
                                                        ],
                                                        label="Contenu",
                                                        required=False,
                                                    ),
                                                ),
                                                (
                                                    "columns",
                                                    wagtail.core.blocks.ListBlock(
                                                        wagtail.core.blocks.StructBlock(
                                                            [
                                                                (
                                                                    "color",
                                                                    wagtail.core.blocks.ChoiceBlock(
                                                                        choices=[
                                                                            (
                                                                                "blue",
                                                                                "Bleue",
                                                                            ),
                                                                            (
                                                                                "pink",
                                                                                "Rose",
                                                                            ),
                                                                            (
                                                                                "white",
                                                                                "Blanche",
                                                                            ),
                                                                            (
                                                                                "none",
                                                                                "Sans couleur",
                                                                            ),
                                                                        ],
                                                                        help_text="Couleur de fond",
                                                                    ),
                                                                ),
                                                                (
                                                                    "paragraph",
                                                                    wagtail.core.blocks.RichTextBlock(
                                                                        features=[
                                                                            "bold",
                                                                            "italic",
                                                                            "link",
                                                                            "h3",
                                                                            "h4",
                                                                            "ol",
                                                                            "ul",
                                                                        ],
                                                                        label="Contenu",
                                                                        required=False,
                                                                    ),
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
                                        label="Sous sections",
                                    ),
                                ),
                            ],
                            label="Section",
                        ),
                    ),
                    ("image", wagtail.images.blocks.ImageChooserBlock()),
                    ("pdf", wagtail.documents.blocks.DocumentChooserBlock()),
                ],
                blank=True,
                help_text="Corps de la page",
                verbose_name="Contenu",
            ),
        ),
        migrations.AlterField(
            model_name="news",
            name="body",
            field=wagtail.core.fields.StreamField(
                [
                    (
                        "heading",
                        wagtail.core.blocks.CharBlock(
                            form_classname="full title", label="Titre de la page"
                        ),
                    ),
                    (
                        "section",
                        wagtail.core.blocks.StructBlock(
                            [
                                (
                                    "color",
                                    wagtail.core.blocks.ChoiceBlock(
                                        choices=[
                                            ("blue", "Bleue"),
                                            ("pink", "Rose"),
                                            ("white", "Blanche"),
                                            ("none", "Sans couleur"),
                                        ],
                                        help_text="Couleur de fond",
                                    ),
                                ),
                                (
                                    "image",
                                    wagtail.images.blocks.ImageChooserBlock(
                                        label="Image à côté du paragraphe",
                                        required=False,
                                    ),
                                ),
                                (
                                    "position",
                                    wagtail.core.blocks.ChoiceBlock(
                                        choices=[
                                            ("right", "Droite"),
                                            ("left", "Gauche"),
                                        ],
                                        help_text="Position de l'image",
                                        required=False,
                                    ),
                                ),
                                (
                                    "paragraph",
                                    wagtail.core.blocks.RichTextBlock(
                                        features=[
                                            "bold",
                                            "italic",
                                            "link",
                                            "h3",
                                            "h4",
                                            "ol",
                                            "ul",
                                            "h2",
                                        ],
                                        label="Contenu",
                                        required=True,
                                    ),
                                ),
                                (
                                    "sub_section",
                                    wagtail.core.blocks.ListBlock(
                                        wagtail.core.blocks.StructBlock(
                                            [
                                                (
                                                    "color",
                                                    wagtail.core.blocks.ChoiceBlock(
                                                        choices=[
                                                            ("blue", "Bleue"),
                                                            ("pink", "Rose"),
                                                            ("white", "Blanche"),
                                                            ("none", "Sans couleur"),
                                                        ],
                                                        help_text="Couleur de fond",
                                                    ),
                                                ),
                                                (
                                                    "paragraph",
                                                    wagtail.core.blocks.RichTextBlock(
                                                        features=[
                                                            "bold",
                                                            "italic",
                                                            "link",
                                                            "h3",
                                                            "h4",
                                                            "ol",
                                                            "ul",
                                                        ],
                                                        label="Contenu",
                                                        required=False,
                                                    ),
                                                ),
                                                (
                                                    "columns",
                                                    wagtail.core.blocks.ListBlock(
                                                        wagtail.core.blocks.StructBlock(
                                                            [
                                                                (
                                                                    "color",
                                                                    wagtail.core.blocks.ChoiceBlock(
                                                                        choices=[
                                                                            (
                                                                                "blue",
                                                                                "Bleue",
                                                                            ),
                                                                            (
                                                                                "pink",
                                                                                "Rose",
                                                                            ),
                                                                            (
                                                                                "white",
                                                                                "Blanche",
                                                                            ),
                                                                            (
                                                                                "none",
                                                                                "Sans couleur",
                                                                            ),
                                                                        ],
                                                                        help_text="Couleur de fond",
                                                                    ),
                                                                ),
                                                                (
                                                                    "paragraph",
                                                                    wagtail.core.blocks.RichTextBlock(
                                                                        features=[
                                                                            "bold",
                                                                            "italic",
                                                                            "link",
                                                                            "h3",
                                                                            "h4",
                                                                            "ol",
                                                                            "ul",
                                                                        ],
                                                                        label="Contenu",
                                                                        required=False,
                                                                    ),
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
                                        label="Sous sections",
                                    ),
                                ),
                            ],
                            label="Section",
                        ),
                    ),
                    ("image", wagtail.images.blocks.ImageChooserBlock()),
                    ("pdf", wagtail.documents.blocks.DocumentChooserBlock()),
                ],
                blank=True,
                help_text="Corps de la page",
                verbose_name="Contenu",
            ),
        ),
        migrations.AlterField(
            model_name="news",
            name="introduction",
            field=wagtail.core.fields.RichTextField(max_length=100),
        ),
        migrations.AlterField(
            model_name="resource",
            name="body",
            field=wagtail.core.fields.StreamField(
                [
                    (
                        "heading",
                        wagtail.core.blocks.CharBlock(
                            form_classname="full title", label="Titre de la page"
                        ),
                    ),
                    (
                        "section",
                        wagtail.core.blocks.StructBlock(
                            [
                                (
                                    "color",
                                    wagtail.core.blocks.ChoiceBlock(
                                        choices=[
                                            ("blue", "Bleue"),
                                            ("pink", "Rose"),
                                            ("white", "Blanche"),
                                            ("none", "Sans couleur"),
                                        ],
                                        help_text="Couleur de fond",
                                    ),
                                ),
                                (
                                    "image",
                                    wagtail.images.blocks.ImageChooserBlock(
                                        label="Image à côté du paragraphe",
                                        required=False,
                                    ),
                                ),
                                (
                                    "position",
                                    wagtail.core.blocks.ChoiceBlock(
                                        choices=[
                                            ("right", "Droite"),
                                            ("left", "Gauche"),
                                        ],
                                        help_text="Position de l'image",
                                        required=False,
                                    ),
                                ),
                                (
                                    "paragraph",
                                    wagtail.core.blocks.RichTextBlock(
                                        features=[
                                            "bold",
                                            "italic",
                                            "link",
                                            "h3",
                                            "h4",
                                            "ol",
                                            "ul",
                                            "h2",
                                        ],
                                        label="Contenu",
                                        required=True,
                                    ),
                                ),
                                (
                                    "sub_section",
                                    wagtail.core.blocks.ListBlock(
                                        wagtail.core.blocks.StructBlock(
                                            [
                                                (
                                                    "color",
                                                    wagtail.core.blocks.ChoiceBlock(
                                                        choices=[
                                                            ("blue", "Bleue"),
                                                            ("pink", "Rose"),
                                                            ("white", "Blanche"),
                                                            ("none", "Sans couleur"),
                                                        ],
                                                        help_text="Couleur de fond",
                                                    ),
                                                ),
                                                (
                                                    "paragraph",
                                                    wagtail.core.blocks.RichTextBlock(
                                                        features=[
                                                            "bold",
                                                            "italic",
                                                            "link",
                                                            "h3",
                                                            "h4",
                                                            "ol",
                                                            "ul",
                                                        ],
                                                        label="Contenu",
                                                        required=False,
                                                    ),
                                                ),
                                                (
                                                    "columns",
                                                    wagtail.core.blocks.ListBlock(
                                                        wagtail.core.blocks.StructBlock(
                                                            [
                                                                (
                                                                    "color",
                                                                    wagtail.core.blocks.ChoiceBlock(
                                                                        choices=[
                                                                            (
                                                                                "blue",
                                                                                "Bleue",
                                                                            ),
                                                                            (
                                                                                "pink",
                                                                                "Rose",
                                                                            ),
                                                                            (
                                                                                "white",
                                                                                "Blanche",
                                                                            ),
                                                                            (
                                                                                "none",
                                                                                "Sans couleur",
                                                                            ),
                                                                        ],
                                                                        help_text="Couleur de fond",
                                                                    ),
                                                                ),
                                                                (
                                                                    "paragraph",
                                                                    wagtail.core.blocks.RichTextBlock(
                                                                        features=[
                                                                            "bold",
                                                                            "italic",
                                                                            "link",
                                                                            "h3",
                                                                            "h4",
                                                                            "ol",
                                                                            "ul",
                                                                        ],
                                                                        label="Contenu",
                                                                        required=False,
                                                                    ),
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
                                        label="Sous sections",
                                    ),
                                ),
                            ],
                            label="Section",
                        ),
                    ),
                    ("image", wagtail.images.blocks.ImageChooserBlock()),
                    ("pdf", wagtail.documents.blocks.DocumentChooserBlock()),
                ],
                blank=True,
                help_text="Corps de la page",
                verbose_name="Contenu",
            ),
        ),
        migrations.DeleteModel(
            name="Map",
        ),
    ]
