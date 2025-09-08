from collections.abc import Generator, Iterable
from typing import Self

from aether import BaseWebElement
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
        self.forwarded_base_class_attribute = "w-full text-sm caption-bottom"
        self.forwarded_class_attribute = attributes.pop("_class", "")
        self.forwarded_attributes = attributes

        super().__init__(
            _class="overflow-x-auto relative w-full",
            data_slot="table-container",
            **attributes,
        )

    def __call__(self, *children: tuple) -> Self:
        forwarded_children = []
        for child in children:
            if (
                isinstance(child, str)
                or isinstance(child, BaseWebElement)
                or not isinstance(child, Iterable)
            ):
                forwarded_children.append(child)
            elif isinstance(child, Generator):
                forwarded_children.extend(list(child))
            elif isinstance(child, type(None)):
                continue
            else:
                forwarded_children.extend(child)

        self.children.append(
            PyTable(
                _class=tw_merge(
                    self.forwarded_base_class_attribute, self.forwarded_class_attribute
                ),
                data_slot="table",
            )(*forwarded_children)
        )

        return self


class TableHeader(Thead):
    def __init__(self, **attributes: Unpack[TheadAttributes]):
        base_class_attribute = "[&_tr]:border-b"

        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            data_slot="table-header",
            **attributes,
        )


class TableBody(Tbody):
    def __init__(self, **attributes: Unpack[TbodyAttributes]):
        base_class_attribute = "[&_tr:last-child]:border-0"

        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            data_slot="table-body",
            **attributes,
        )


class TableFooter(Tfoot):
    def __init__(self, **attributes: Unpack[TfootAttributes]):
        base_class_attribute = "font-medium bg-muted/50 border-t [&>tr]:last:border-b-0"

        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            data_slot="table-footer",
            **attributes,
        )


class TableRow(Tr):
    def __init__(self, **attributes: Unpack[TrAttributes]):
        base_class_attribute = "border-b transition-colors data-[state=selected]:bg-muted hover:bg-muted/50"

        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            data_slot="table-row",
            **attributes,
        )


class TableHead(Th):
    def __init__(self, **attributes: Unpack[ThAttributes]):
        base_class_attribute = "align-middle px-2 h-10 font-medium text-foreground text-left whitespace-nowrap [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-[2px]"

        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            data_slot="table-head",
            **attributes,
        )


class TableCell(Td):
    def __init__(self, **attributes: Unpack[TdAttributes]):
        base_class_attribute = "align-middle p-2 whitespace-nowrap [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-[2px]"

        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            data_slot="table-cell",
            **attributes,
        )


class TableCaption(Caption):
    def __init__(self, **attributes: Unpack[CaptionAttributes]):
        base_class_attribute = "mt-4 text-muted-foreground text-sm"

        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            data_slot="table-caption",
            **attributes,
        )
