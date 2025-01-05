from pytempl.plugins.tailwindcss import tw_merge
from pytempl.tags.html import (
    ButtonAttributes as PyButtonAttributes,
)
from pytempl.tags.html import (
    Li,
    LiAttributes,
    Nav,
    NavAttributes,
    Span,
    SpanAttributes,
    Ul,
    UlAttributes,
)
from pytempl_icons import ChevronLeftIcon, ChevronRightIcon, EllipsisIcon

from .button import Button, ButtonVariant

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class Pagination(Nav):
    def __init__(self, number_of_pages: int, **attributes: Unpack[NavAttributes]):
        base_class_attribute = "flex w-full mx-auto"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(class_attribute, base_class_attribute),
            role="navigation",
            aria_label="pagination",
            x_data=f"{{ numberOfPages: {number_of_pages}, currentPageIndex: 1, previousPage() {{if (this.currentPageIndex > 1) {{this.currentPageIndex = this.currentPageIndex - 1}} }}, nextPage() {{if (this.currentPageIndex < this.numberOfPages) {{this.currentPageIndex = this.currentPageIndex + 1}} }} }}",
            **attributes,
        )


class PaginationContent(Ul):
    def __init__(self, **attributes: Unpack[UlAttributes]):
        base_class_attribute = "flex flex-row items-center gap-1"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(class_attribute, base_class_attribute),
            **attributes,
        )


class PaginationItem(Li):
    def __init__(self, item_index: int | None, **attributes: Unpack[LiAttributes]):
        base_class_attribute = ""
        class_attribute = attributes.pop("_class", "")

        if item_index is not None:
            page_index = item_index + 1

            super().__init__(
                _class=tw_merge(class_attribute, base_class_attribute),
                x_data=f"{{ pageIndex: {page_index} }}",
                **attributes,
            )
        else:
            super().__init__(
                _class=tw_merge(class_attribute, base_class_attribute),
                **attributes,
            )


class PaginationLink(Button):
    def __init__(self, **attributes: Unpack[PyButtonAttributes]):
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            size="icon",
            variant="ghost",
            _class=class_attribute,
            **{
                "@click": "currentPageIndex = pageIndex",
                ":aria-current": "currentPageIndex === pageIndex ? 'page' : undefined",
                ":class": f"currentPageIndex === pageIndex && '{ButtonVariant['outline'].value}'",
            },
            **attributes,
        )


class PaginationPrevious(Button):
    def __init__(self, **attributes: Unpack[PyButtonAttributes]):
        base_class_attribute = "gap-1 pl-2.5"
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

        self.children = [
            ChevronLeftIcon(_class="h-4 w-4"),
            "Previous",
        ]


class PaginationNext(Button):
    def __init__(self, **attributes: Unpack[PyButtonAttributes]):
        base_class_attribute = "gap-1 pr-2.5"
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

        self.children = ["Next", ChevronRightIcon(_class="h-4 w-4")]


class PaginationEllipsis(Span):
    def __init__(self, **attributes: Unpack[SpanAttributes]):
        base_class_attribute = "flex h-9 w-9 items-center justify-center"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            aria_hidden=True,
            _class=tw_merge(class_attribute, base_class_attribute),
            **attributes,
        )

        self.children = [
            EllipsisIcon(_class="h-4 w-4"),
            Span(_class="sr-only")("More pages"),
        ]
