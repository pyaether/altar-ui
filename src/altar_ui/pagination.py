import warnings
from typing import Self

from aether.plugins.alpinejs import AlpineJSData, Statement, alpine_js_data_merge
from aether.plugins.tailwindcss import tw_merge
from aether.tags.html import (
    ButtonAttributes as PyButtonAttributes,
)
from aether.tags.html import (
    Li,
    LiAttributes,
    Nav,
    NavAttributes,
    Span,
    SpanAttributes,
    Ul,
    UlAttributes,
)
from altar_icons import ChevronLeftIcon, ChevronRightIcon, EllipsisIcon

from .button import Button, ButtonVariant

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack  # noqa: UP035


class Pagination(Nav):
    def __init__(self, number_of_pages: int, **attributes: Unpack[NavAttributes]):
        base_class_attribute = "flex justify-center mx-auto w-full"
        base_x_data_attribute = AlpineJSData(
            data={
                "numberOfPages": number_of_pages,
                "currentPageIndex": 1,
                "previousPage()": Statement(
                    "{ if (this.currentPageIndex > 1) { this.currentPageIndex -= 1 } }",
                    seq_type="definition",
                ),
                "nextPage()": Statement(
                    "{ if (this.currentPageIndex < this.numberOfPages) { this.currentPageIndex += 1 } }",
                    seq_type="definition",
                ),
            },
            directive="x-data",
        )
        class_attribute = attributes.pop("_class", "")
        x_data_attribute = attributes.pop("x_data", None)

        super().__init__(
            _class=tw_merge(class_attribute, base_class_attribute),
            role="navigation",
            aria_label="pagination",
            x_data=alpine_js_data_merge(base_x_data_attribute, x_data_attribute),
            data_slot="pagination",
            **attributes,
        )


class PaginationContent(Ul):
    def __init__(self, **attributes: Unpack[UlAttributes]):
        base_class_attribute = "flex flex-row gap-1 items-center"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(class_attribute, base_class_attribute),
            data_slot="pagination-content",
            **attributes,
        )


class PaginationItem(Li):
    def __init__(
        self, item_index: int | None = None, **attributes: Unpack[LiAttributes]
    ):
        class_attribute = attributes.pop("_class", "")

        if item_index is not None:
            base_x_data_attribute = AlpineJSData(
                data={
                    "pageIndex": item_index + 1,
                    "isActive()": Statement(
                        "{ if (currentPageIndex === this.pageIndex) { return true } else { return false } }",
                        seq_type="definition",
                    ),
                    "setActive()": Statement(
                        "{ currentPageIndex = this.pageIndex }",
                        seq_type="definition",
                    ),
                },
                directive="x-data",
            )
            x_data_attribute = attributes.pop("x_data", None)

            super().__init__(
                _class=class_attribute,
                x_data=alpine_js_data_merge(base_x_data_attribute, x_data_attribute),
                data_slot="pagination-item",
                **attributes,
            )
        else:
            super().__init__(
                _class=class_attribute, data_slot="pagination-item", **attributes
            )


class PaginationLink(Button):
    def __init__(self, **attributes: Unpack[PyButtonAttributes]):
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            size="icon",
            variant=None,
            _class=class_attribute,
            data_slot="pagination-link",
            **{
                "@click": "setActive()",
                ":aria-current": "isActive() ? 'page' : undefined",
                ":data-active": "isActive()",
                ":class": f"isActive() ? '{ButtonVariant.outline}' : '{ButtonVariant.ghost}'",
            },
            **attributes,
        )


class PaginationPrevious(Button):
    def __init__(self, **attributes: Unpack[PyButtonAttributes]):
        base_class_attribute = "gap-1 px-2.5 sm:pl-2.5"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            aria_label="Go to previous page",
            size="default",
            type="button",
            _class=tw_merge(class_attribute, base_class_attribute),
            **{
                "@click": "previousPage()",
                ":disabled": "currentPageIndex === 1",
            },
            **attributes,
        )

        self.children = [ChevronLeftIcon(), Span(_class="hidden sm:block")("Previous")]

    def __call__(self, *_children: tuple) -> Self:
        warnings.warn(
            f"Trying to add child to a non-child element: {self.__class__.__qualname__}",
            UserWarning,
            stacklevel=2,
        )

        return self


class PaginationNext(Button):
    def __init__(self, **attributes: Unpack[PyButtonAttributes]):
        base_class_attribute = "gap-1 px-2.5 sm:pr-2.5"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            aria_label="Go to next page",
            size="default",
            type="button",
            _class=tw_merge(class_attribute, base_class_attribute),
            **{
                "@click": "nextPage()",
                ":disabled": "currentPageIndex === numberOfPages",
            },
            **attributes,
        )

        self.children = [Span(_class="hidden sm:block")("Next"), ChevronRightIcon()]

    def __call__(self, *_children: tuple) -> Self:
        warnings.warn(
            f"Trying to add child to a non-child element: {self.__class__.__qualname__}",
            UserWarning,
            stacklevel=2,
        )

        return self


class PaginationEllipsis(Span):
    def __init__(self, **attributes: Unpack[SpanAttributes]):
        base_class_attribute = "flex justify-center items-center size-9"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            aria_hidden=True,
            data_slot="pagination-ellipsis",
            _class=tw_merge(class_attribute, base_class_attribute),
            **attributes,
        )

        self.children = [
            EllipsisIcon(),
            Span(_class="sr-only")("More pages"),
        ]

    def __call__(self, *_children: tuple) -> Self:
        warnings.warn(
            f"Trying to add child to a non-child element: {self.__class__.__qualname__}",
            UserWarning,
            stacklevel=2,
        )

        return self
