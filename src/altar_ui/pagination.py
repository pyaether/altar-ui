"""Pagination

Pagination with page navigation, next and previous links.

Composition:
    Use the following composition to build a Pagination:

    Pagination
    ├── PaginationItem
    │   └── PaginationPrevious
    ├── PaginationItem
    │   └── PaginationLink
    ├── PaginationItem
    │   └── ... ellipsis_icon, etc.
    └── PaginationItem
        └── PaginationNext
"""

import warnings
from typing import Self

from aether.plugins.tailwindcss import tw_merge
from aether.tags.html import (
    A,
    AAttributes,
    Li,
    LiAttributes,
    Ul,
    UlAttributes,
)
from altar_icons import ChevronLeftIcon, ChevronRightIcon

from .button import ButtonSize, ButtonVariant

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack  # noqa: UP035


class Pagination(Ul):
    def __init__(self, **attributes: Unpack[UlAttributes]):
        base_class_attribute = "flex-wrap break-words items-center text-muted-foreground text-sm gap-1.5 flex sm:gap-2.5"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            role="navigation",
            aria_label="pagination",
            **attributes,
        )


class PaginationItem(Li):
    def __init__(self, **attributes: Unpack[LiAttributes]):
        base_class_attribute = "inline-flex items-center gap-1.5"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            **attributes,
        )


class PaginationLink(A):
    def __init__(
        self,
        is_active: bool = False,
        disabled: bool = False,
        **attributes: Unpack[AAttributes],
    ):
        variant_class_attribute = (
            ButtonVariant["outline"] if is_active else ButtonVariant["ghost"]
        )
        size_class_attribute = ButtonSize["icon"]
        base_class_attribute = "outline-none whitespace-nowrap inline-flex transition-all transition-colors justify-center rounded-md cursor-pointer shrink-0 items-center font-medium text-sm aria-invalid:border-destructive aria-invalid:ring-destructive/20 hover:text-foreground focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px] disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:shrink-0 [&_svg:not([class*='size-'])]:size-4 dark:aria-invalid:ring-destructive/40"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(
                variant_class_attribute,
                size_class_attribute,
                base_class_attribute,
                class_attribute,
            ),
            aria_current="page" if is_active else "false",
            aria_disabled="true" if disabled else "false",
            **attributes,
        )


class PaginationPrevious(A):
    def __init__(self, disabled: bool = False, **attributes: Unpack[AAttributes]):
        variant_class_attribute = ButtonVariant["ghost"]
        size_class_attribute = ButtonSize["default"]
        base_class_attribute = "outline-none whitespace-nowrap inline-flex transition-all transition-colors justify-center rounded-md cursor-pointer shrink-0 items-center font-medium text-sm aria-invalid:border-destructive aria-invalid:ring-destructive/20 hover:text-foreground focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px] disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:shrink-0 [&_svg:not([class*='size-'])]:size-4 dark:aria-invalid:ring-destructive/40"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(
                variant_class_attribute,
                size_class_attribute,
                base_class_attribute,
                class_attribute,
            ),
            aria_label="Go to previous page",
            aria_disabled="true" if disabled else "false",
            **attributes,
        )

        self.children = [ChevronLeftIcon(), "Previous"]

    def __call__(self, *_children: tuple) -> Self:
        warnings.warn(
            f"Trying to add child to a non-child element: {self.__class__.__qualname__}",
            UserWarning,
            stacklevel=2,
        )

        return self


class PaginationNext(A):
    def __init__(self, disabled: bool = False, **attributes: Unpack[AAttributes]):
        variant_class_attribute = ButtonVariant["ghost"]
        size_class_attribute = ButtonSize["default"]
        base_class_attribute = "outline-none whitespace-nowrap inline-flex transition-all transition-colors justify-center rounded-md cursor-pointer shrink-0 items-center font-medium text-sm aria-invalid:border-destructive aria-invalid:ring-destructive/20 hover:text-foreground focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px] disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:shrink-0 [&_svg:not([class*='size-'])]:size-4 dark:aria-invalid:ring-destructive/40"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(
                variant_class_attribute,
                size_class_attribute,
                base_class_attribute,
                class_attribute,
            ),
            aria_label="Go to next page",
            aria_disabled="true" if disabled else "false",
            **attributes,
        )

        self.children = ["Next", ChevronRightIcon()]

    def __call__(self, *_children: tuple) -> Self:
        warnings.warn(
            f"Trying to add child to a non-child element: {self.__class__.__qualname__}",
            UserWarning,
            stacklevel=2,
        )

        return self
