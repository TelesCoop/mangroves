# image_formats.py
from django.utils.html import format_html
from wagtail.images.formats import (
    Format,
    unregister_image_format,
    register_image_format,
)


class CaptionedImageFormat(Format):
    def image_to_html(self, image, alt_text, extra_attributes=None):

        default_html = super().image_to_html(image, alt_text, extra_attributes)

        return format_html(
            "{}<figcaption class='image-caption'>{}</figcaption>",
            default_html,
            image.caption,
        )


unregister_image_format("fullwidth")
unregister_image_format("left")
unregister_image_format("right")

register_image_format(
    CaptionedImageFormat("fullwidth", "", "bodytext-image", "width-750")
)
register_image_format(
    CaptionedImageFormat("left", "", "bodytext-image small left", "width-400")
)
register_image_format(
    CaptionedImageFormat("right", "", "bodytext-image small right", "width-400")
)
