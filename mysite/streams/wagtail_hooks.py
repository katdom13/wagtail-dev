"""
Hooks to extend the richtext blocks in wagtail
"""
import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.admin.rich_text.converters.html_to_contentstate import (
    InlineStyleElementHandler,
)
from wagtail.core import hooks


@hooks.register("register_rich_text_features")
def register_code_styling(features):
    """
    Adds the <code> feature to the richtext editor and page
    """

    # Step 1
    feature_name = "code"
    type_ = "CODE"
    tag = "code"  # <code></code>

    # Step 2 - What you see in the admin editor
    control = {
        "type": type_,
        "label": "</>",
        "description": "Code"
    }

    # Step 3 - Register control in the admin editor
    features.register_editor_plugin(
        "draftail",
        feature_name,
        draftail_features.InlineStyleFeature(control)
    )

    # Step 4 - What you see in the pages, outside the admin editor
    db_conversion = {
        "from_database_format": {
            tag: InlineStyleElementHandler(type_),
        },
        "to_database_format": {
            "style_map": {
                type_: {
                    "element": tag
                }
            }
        }
    }

    # Step 5 - Register to rule converter
    features.register_converter_rule("contentstate", feature_name, db_conversion)

    # Step 6 - Optional; Enable this feature for ALL instances of the
    # richtext editor throughtout the website
    features.default_features.append(feature_name)


@hooks.register("register_rich_text_features")
def register_centertext_feature(features):
    """
    Creates centered text in the richtext editor and page
    """

    # Step 1
    feature_name = "center"
    type_ = "CENTERTEXT"
    tag = "div"  # <div style="display: block; text-align: center;"></div>

    # Step 2 - What you see in the admin editor
    control = {
        "type": type_,
        "label": "Center",
        "description": "Center Text",
        "style": {
            "display": "block",
            "text-align": "center",
        },
    }

    # Step 3 - Register control in the admin editor
    features.register_editor_plugin(
        "draftail",
        feature_name,
        draftail_features.InlineStyleFeature(control)
    )

    # Step 4 - What you see in the pages, outside the admin editor
    db_conversion = {
        "from_database_format": {
            tag: InlineStyleElementHandler(type_)
        },
        "to_database_format": {
            "style_map": {
                type_: {
                    "element": tag,
                    "props": {
                        "class": "d-block text-center"
                    }
                }
            }
        }
    }

    # Step 5 - Register to rule converter
    features.register_converter_rule("contentstate", feature_name, db_conversion)

    # Step 6 - Optional; Enable this feature for ALL instances of the
    # richtext editor throughtout the website
    features.default_features.append(feature_name)
