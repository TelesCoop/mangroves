from django.templatetags.static import static
from django.utils.html import format_html
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)
from wagtail.core import hooks
from wagtail.contrib.modeladmin.views import EditView, CreateView

from mangmap.models.country import WorldZone, Country
from mangmap.models.models import Thematic, ActualityType, SiteType
from mangmap.models.news import News
from mangmap.models.site import Site


@hooks.register("insert_global_admin_css", order=100)
def global_admin_css():
    """Add /static/css/mangmap-admin.css to the admin."""
    return format_html(
        '<link rel="stylesheet" href="{}">', static("css/mangmap-admin.css")
    )


class RelatedCountriesEditView(EditView):
    def dispatch(self, request, *args, **kwargs):
        to_return = super().dispatch(request, *args, **kwargs)
        instance: Site = self.instance
        instance.add_countries_from_zone()
        return to_return


class RelatedCountriesCreateView(CreateView):
    def dispatch(self, request, *args, **kwargs):
        to_return = super().dispatch(request, *args, **kwargs)
        try:
            instance: Site = self.get_instance()
            instance.add_countries_from_zone()
        except ValueError:
            pass
        return to_return


class SiteModelAdmin(ModelAdmin):
    model = Site
    menu_label = "Sites"
    menu_icon = "folder-inverse"
    add_to_settings_menu = False
    search_fields = ("name",)

    edit_view_class = RelatedCountriesEditView
    create_view_class = RelatedCountriesCreateView


class ThematicModelAdmin(ModelAdmin):
    model = Thematic
    menu_label = "Thématiques"
    menu_icon = "tag"
    add_to_settings_menu = False
    search_fields = ("name",)
    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
        FieldPanel("icon"),
    ]


class SiteTypeModelAdmin(ModelAdmin):
    model = SiteType
    menu_label = "Types de site"
    menu_icon = "tag"
    add_to_settings_menu = False
    search_fields = ("name",)


class SitesAdminGroup(ModelAdminGroup):
    menu_label = "Sites"
    menu_order = 201
    menu_icon = "doc-full"
    items = (SiteModelAdmin, ThematicModelAdmin, SiteTypeModelAdmin)


class NewsModelAdmin(ModelAdmin):
    model = News
    menu_label = "Actualités"
    menu_icon = "folder-inverse"
    add_to_settings_menu = False
    search_fields = ("name",)

    edit_view_class = RelatedCountriesEditView
    create_view_class = RelatedCountriesCreateView


class ActualityTypeModelAdmin(ModelAdmin):
    model = ActualityType
    menu_label = "Types d'actualité"
    menu_icon = "tag"
    add_to_settings_menu = False
    search_fields = ("name",)


class ActualityAdminGroup(ModelAdminGroup):
    menu_label = "Actualités"
    menu_order = 202
    menu_icon = "date"
    items = (NewsModelAdmin, ActualityTypeModelAdmin)


class WorldZoneModelAdmin(ModelAdmin):
    model = WorldZone
    menu_label = "Zones du monde"
    menu_icon = "site"
    add_to_settings_menu = False
    search_fields = ("name",)


class CountryModelAdmin(ModelAdmin):
    model = Country
    menu_label = "Pays"
    menu_icon = "site"
    add_to_settings_menu = False
    search_fields = ("name",)


class GeneralAdminGroup(ModelAdminGroup):
    menu_label = "Général"
    menu_order = 203
    menu_icon = "cogs"
    items = (CountryModelAdmin, WorldZoneModelAdmin)


modeladmin_register(SitesAdminGroup)
modeladmin_register(ActualityAdminGroup)
modeladmin_register(GeneralAdminGroup)