"""Table

A responsive table component.

Composition:
    Use the following composition to build a Table:

    Table
    ├── TableCaption (optional)
    ├── TableHeader
    │   └── TableRow
    │       └── TableHead
    ├── TableBody
    │   ├── TableRow
    │   │   └── TableCell
    │   └── TableRow
    │       └── TableCell
    └── TableFooter (optional)
        └── TableRow
            └── TableCell
"""

from typing import Self

from aether.plugins.tailwindcss import tw_merge
from aether.tags.html import (
    Caption,
    CaptionAttributes,
    Div,
    Tbody,
    TbodyAttributes,
    Td,
    TdAttributes,
    Tfoot,
    TfootAttributes,
    Th,
    ThAttributes,
    Thead,
    TheadAttributes,
    Tr,
    TrAttributes,
)
from aether.tags.html import Table as PyTable
from aether.tags.html import TableAttributes as PyTableAttributes

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack  # noqa: UP035


class Table(Div):
    def __init__(self, **attributes: Unpack[PyTableAttributes]):
        self.forwarded_base_class_attribute = "text-sm w-full caption-bottom"
        self.forwarded_class_attribute = attributes.pop("_class", "")
        self.forwarded_attributes = attributes

        super().__init__(_class="overflow-x-auto", **attributes)

    def __call__(self, *children: tuple) -> Self:
        self.children.append(
            PyTable(
                _class=tw_merge(
                    self.forwarded_base_class_attribute, self.forwarded_class_attribute
                ),
            )(*children)
        )

        return self


class TableHeader(Thead):
    def __init__(self, **attributes: Unpack[TheadAttributes]):
        base_class_attribute = "[&_tr]:border-b"

        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute), **attributes
        )


class TableBody(Tbody):
    def __init__(self, **attributes: Unpack[TbodyAttributes]):
        base_class_attribute = "[&_tr:last-child]:border-0"

        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute), **attributes
        )


class TableFooter(Tfoot):
    def __init__(self, **attributes: Unpack[TfootAttributes]):
        base_class_attribute = "border-t font-medium bg-muted/50 [&>tr]:last:border-b-0"

        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute), **attributes
        )


class TableRow(Tr):
    def __init__(self, **attributes: Unpack[TrAttributes]):
        base_class_attribute = "transition-colors border-b hover:bg-muted/50"

        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute), **attributes
        )


class TableHead(Th):
    def __init__(self, **attributes: Unpack[ThAttributes]):
        base_class_attribute = "whitespace-nowrap align-middle font-medium text-foreground text-left px-2 h-10 [&>[role=checkbox]]:translate-y-[2px] [&:has([role=checkbox])]:pr-0"

        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute), **attributes
        )


class TableCell(Td):
    def __init__(self, **attributes: Unpack[TdAttributes]):
        base_class_attribute = "whitespace-nowrap align-middle p-2 [&>[role=checkbox]]:translate-y-[2px] [&:has([role=checkbox])]:pr-0"

        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute), **attributes
        )


class TableCaption(Caption):
    def __init__(self, **attributes: Unpack[CaptionAttributes]):
        base_class_attribute = "text-muted-foreground text-sm mt-4"

        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute), **attributes
        )
