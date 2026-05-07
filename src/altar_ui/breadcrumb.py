"""Breadcrumb

Displays the path to the current resource using a hierarchy of links.

Composition:
    Use the following composition to build a Breadcrumb:

    Breadcrumb
    ├── BreadcrumbItem
    │   ├── BreadcrumbLink
    │   └── BreadcrumbPage
    └── BreadcrumbSeparator
"""

from aether.plugins.tailwindcss import tw_merge
from aether.tags.html import (
    A,
    AAttributes,
    Li,
    LiAttributes,
    Ol,
    OlAttributes,
    Span,
    SpanAttributes,
)
from altar_icons import ChevronRightIcon

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack  # noqa: UP035


class Breadcrumb(Ol):
    def __init__(self, **attributes: Unpack[OlAttributes]):
        base_class_attribute = "flex-wrap break-words items-center text-muted-foreground text-sm gap-1.5 flex sm:gap-2.5"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            role="navigation",
            aria_label="breadcrumb",
            **attributes,
        )


class BreadcrumbItem(Li):
    def __init__(self, **attributes: Unpack[LiAttributes]):
        base_class_attribute = "inline-flex items-center gap-1.5"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            **attributes,
        )


class BreadcrumbLink(A):
    def __init__(self, disabled: bool = False, **attributes: Unpack[AAttributes]):
        base_class_attribute = "transition-colors hover:text-foreground"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            aria_disabled="true" if disabled else "false",
            **attributes,
        )


class BreadcrumbPage(Span):
    def __init__(self, **attributes: Unpack[SpanAttributes]):
        base_class_attribute = "font-normal text-foreground"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            aria_current="page",
            aria_disabled="true",
            role="link",
            **attributes,
        )


class BreadcrumbSeparator(Li):
    def __init__(self, **attributes: Unpack[LiAttributes]):
        super().__init__(
            role="presentation",
            aria_hidden="true",
            **attributes,
        )

        self.children = [ChevronRightIcon(_class="size-3.5")]
