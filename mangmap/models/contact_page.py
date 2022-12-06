from typing import List

from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.template.response import TemplateResponse
from wagtail.admin.panels import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page

from mangmap.forms import ContactForm
from mangmap.models.utils import SIMPLE_RICH_TEXT_FIELD_FEATURE


class ContactPage(Page):
    class Meta:
        verbose_name = "Page de contact"

    parent_page_types = ["mangmap.HomePage"]
    subpage_types: List[str] = []
    max_count_per_parent = 1

    left_column = RichTextField(
        features=SIMPLE_RICH_TEXT_FIELD_FEATURE + ["h2", "h3", "h4", "ol", "ul"],
        verbose_name="colonne de gauche",
    )

    content_panels = Page.content_panels + [
        FieldPanel("left_column"),
    ]

    def serve(self, request, *args, **kwargs):
        if request.method == "POST":
            form = ContactForm(request.POST)
            form.full_clean()
            if not form["agree"]:
                form.add_error(
                    "agree",
                    ValidationError("Vous devez accepter les conditions d'utilisation"),
                )
        else:
            form = ContactForm(request.POST)

        context = self.get_context(request, *args, **kwargs)
        context["form"] = form
        context["review_selected"] = bool(request.GET.get("review"))
        return TemplateResponse(
            request,
            "mangmap/contact_page.html",
            context,
        )
