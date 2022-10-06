from django.templatetags.static import static
from django.utils.html import format_html
from wagtail.core import hooks


# Order determines the order of the element
@hooks.register("insert_global_admin_css", order=100)
def global_admin_css():
    """
    Add /static/css/custom.css to the admin site
    """
    return format_html(
        "<link rel='stylesheet' href='{}'>",
        static("css/custom.css")
    )


@hooks.register("insert_global_admin_js", order=100)
def global_admin_js():
    """
    Add /static/js/custom.js to the admin site
    """
    return format_html(
        "<script src='{}'></script>",
        static("js/custom.js")
    )
