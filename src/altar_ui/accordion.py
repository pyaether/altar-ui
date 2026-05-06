"""Accordion

A vertically stacked set of interactive headings that each reveal a section of content.

Composition:
    Use the following composition to build an Accordion:

    Accordion
    ├── AccordionItem
    │   ├── AccordionTrigger
    │   └── AccordionContent
    └── AccordionItem
        ├── AccordionTrigger
        └── AccordionContent
"""

from enum import StrEnum
from typing import Literal, Self

from aether.plugins.alpinejs import AlpineJSData, Statement, alpine_js_data_merge
from aether.plugins.tailwindcss import tw_merge
from aether.tags.html import (
    Details,
    DetailsAttributes,
    Div,
    DivAttributes,
    Summary,
    SummaryAttributes,
)
from altar_icons import ChevronDownIcon

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack  # noqa: UP035


class AccordionType(StrEnum):
    single = AlpineJSData(
        data={
            "activeAccordion": "",
            "isActive(id)": Statement(
                "{ return this.activeAccordion === id }", seq_type="definition"
            ),
            "toggleActiveAccordionState(id)": Statement(
                "{ this.activeAccordion = (this.isActive(id)) ? '' : id }",
                seq_type="definition",
            ),
        },
        directive="x-data",
    )
    multiple = AlpineJSData(
        data={
            "activeAccordions": [],
            "isActive(id)": Statement(
                "{ return this.activeAccordions.includes(id) }", seq_type="definition"
            ),
            "toggleActiveAccordionState(id)": Statement(
                "{ this.isActive(id) ? this.activeAccordions = this.activeAccordions.filter(i => i !== id) : this.activeAccordions.push(id) }",
                seq_type="definition",
            ),
        },
        directive="x-data",
    )


class Accordion(Div):
    def __init__(
        self, type: Literal["single", "multiple"], **attributes: Unpack[DivAttributes]
    ):
        base_x_data_attribute = AccordionType[type]
        x_data_attribute = attributes.pop("x_data", None)

        super().__init__(
            x_data=alpine_js_data_merge(base_x_data_attribute, x_data_attribute),
            **attributes,
        )


class AccordionItem(Details):
    def __init__(self, **attributes: Unpack[DetailsAttributes]):
        if attributes.get("id"):
            id_attribute = attributes.pop("id")
        elif attributes.get(":id"):
            id_attribute = attributes.pop(":id")
        else:
            id_attribute = "$id('accordion-item')"

        closed_state_class_attributes = "[&::details-content]:[block-size:0] [&::details-content]:block [&::details-content]:opacity-0 [&::details-content]:transition-discrete [&::details-content]:transition-all"
        open_state_class_attributes = "open:[&::details-content]:[block-size:auto] open:[&::details-content]:[block-size:calc-size(auto,size)] open:[&::details-content]:opacity-100"

        base_class_attribute = "border-b group last:border-b-0"
        base_x_data_attribute = AlpineJSData(
            data={
                "item_id": Statement(content=id_attribute, seq_type="assignment")
                if "$id" in id_attribute
                else id_attribute.lower().replace(" ", "-"),
            },
            directive="x-data",
        )
        x_data_attribute = attributes.pop("x_data", None)
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(
                closed_state_class_attributes,
                open_state_class_attributes,
                base_class_attribute,
                class_attribute,
            ),
            x_data=alpine_js_data_merge(base_x_data_attribute, x_data_attribute),
            **{":open": "isActive(item_id)"},
            **attributes,
        )


class AccordionTrigger(Summary):
    def __init__(self, **attributes: Unpack[SummaryAttributes]):
        base_class_attribute = "outline-none transition-all justify-between rounded-md items-center flex-1 gap-4 flex py-4 w-full focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px]"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            **{"@click.prevent": "toggleActiveAccordionState(item_id)"},
            **attributes,
        )

    def __call__(self, *children: tuple) -> Self:
        super().__call__(*children)

        self.children.append(
            ChevronDownIcon(
                _class="pointer-events-none translate-y-0.5 transition-transform duration-200 shrink-0 text-muted-foreground size-4 group-open:rotate-180"
            )
        )

        return self


class AccordionContent(Div):
    def __init__(self, **attributes: Unpack[DivAttributes]):
        base_class_attribute = "pb-4"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            **attributes,
        )
