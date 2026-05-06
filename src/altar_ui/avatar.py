"""Avatar

An image element with a fallback for representing the user.

Composition:
    Use the following composition to build an Avatar:

    Avatar
    ├── AvatarImage
    └── AvatarFallback
"""

from aether.plugins.alpinejs import AlpineJSData, Statement, alpine_js_data_merge
from aether.plugins.tailwindcss import tw_merge
from aether.tags.html import Img, ImgAttributes, Span, SpanAttributes

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack  # noqa: UP035


class Avatar(Span):
    def __init__(self, **attributes: Unpack[SpanAttributes]):
        base_class_attribute = (
            "relative flex size-8 shrink-0 overflow-hidden rounded-full"
        )
        base_x_data_attribute = AlpineJSData(
            data={"status": "loading"}, directive="x-data"
        )

        class_attribute = attributes.pop("_class", "")
        x_data_attribute = attributes.pop("x_data", None)

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            x_data=alpine_js_data_merge(base_x_data_attribute, x_data_attribute),
            **attributes,
        )


class AvatarImage(Img):
    def __init__(self, **attributes: Unpack[ImgAttributes]):
        base_class_attribute = "size-full aspect-square"
        base_x_init_attribute = AlpineJSData(
            data={
                "check_cache": Statement(
                    content="status = $el.complete ? ($el.naturalWidth ? 'loaded' : 'error') : status",
                    seq_type="instance",
                )
            },
            directive="x-init",
        )

        class_attribute = attributes.pop("_class", "")
        x_init_attribute = attributes.pop("x_init", None)

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            x_init=alpine_js_data_merge(base_x_init_attribute, x_init_attribute),
            x_cloak=True,
            x_show="status === 'loaded'",
            **{"@load": "status = 'loaded'", "@error": "status = 'error'"},
            **attributes,
        )


class AvatarFallback(Span):
    def __init__(self, **attributes: Unpack[SpanAttributes]):
        base_class_attribute = "justify-center items-center size-full flex bg-muted"

        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            x_cloak=True,
            x_show="status !== 'loaded'",
            **attributes,
        )
