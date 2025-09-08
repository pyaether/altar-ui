import warnings
from typing import Self

from aether.plugins.tailwindcss import tw_merge
from aether.tags.html import (
    A,
    AAttributes,
    Li,
    LiAttributes,
    Nav,
    NavAttributes,
    Ol,
    OlAttributes,
    Span,
    SpanAttributes,
)
from altar_icons import BaseSVGIconElement, ChevronRightIcon, EllipsisIcon

from .passthrough import Passthrough

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack  # noqa: UP035


class Breadcrumb(Nav):
    def __init__(self, **attributes: Unpack[NavAttributes]):
        super().__init__(data_slot="breadcrumb", aria_label="breadcrumb", **attributes)


class BreadcrumbList(Ol):
    def __init__(self, **attributes: Unpack[OlAttributes]):
        base_class_attribute = "flex flex-wrap gap-1.5 items-center text-muted-foreground text-sm break-words sm:gap-2.5"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            data_slot="breadcrumb-list",
            **attributes,
        )


class BreadcrumbItem(Li):
    def __init__(self, **attributes: Unpack[LiAttributes]):
        base_class_attribute = "inline-flex gap-1.5 items-center"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            data_slot="breadcrumb-item",
            **attributes,
        )


class BreadcrumbLink(A):
    def __init__(self, pass_through: bool = False, **attributes: Unpack[AAttributes]):
        base_class_attribute = "transition-colors hover:text-foreground"
        class_attribute = attributes.pop("_class", "")

        data_slot = attributes.pop("data_slot", "breadcrumb-link")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            data_slot=data_slot,
            **attributes,
        )

        self.pass_through = pass_through

    def __call__(self, *children: tuple) -> Self | Passthrough:
        if self.pass_through:
            return Passthrough(**self.attributes)(*children)
        else:
            return super().__call__(*children)


class BreadcrumbPage(Span):
    def __init__(self, **attributes: Unpack[SpanAttributes]):
        base_class_attribute = "font-normal text-foreground"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            data_slot="breadcrumb-page",
            role="link",
            aria_disabled="true",
            aria_current="page",
            **attributes,
        )


class BreadcrumbSeparator(Li):
    def __init__(self, **attributes: Unpack[LiAttributes]):
        base_class_attribute = "[&>svg]:size-3.5"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            data_slot="breadcrumb-separator",
            role="presentation",
            aria_hidden="true",
            **attributes,
        )

        self.children = [ChevronRightIcon()]

    def __call__(self, *children: tuple) -> Self:
        allowed_child_types = (str, BaseSVGIconElement)

        if len(children) != 1:
            raise ValueError(
                f"`{self.__class__.__qualname__}` must be called with exactly one child, but got {len(children)}."
            )
        else:
            child = children[0]
            if isinstance(child, allowed_child_types):
                self.children = [child]
            else:
                raise ValueError(
                    f"Invalid child type found. `{self.__class__.__qualname__}` can only have {', '.join([type(allowed_type).__class__.__qualname__ for allowed_type in allowed_child_types])}."
                )

        return self


class BreadcrumbEllipsis(Span):
    def __init__(self, **attributes: Unpack[SpanAttributes]):
        base_class_attribute = "flex justify-center items-center size-9"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            data_slot="breadcrumb-ellipsis",
            role="presentation",
            aria_hidden="true",
            **attributes,
        )

        self.children = [EllipsisIcon(_class="size-4"), Span(_class="sr-only")("More")]

    def __call__(self, *_children: tuple) -> Self:
        warnings.warn(
            f"Trying to add child to a non-child element: {self.__class__.__qualname__}",
            UserWarning,
            stacklevel=2,
        )

        return self
