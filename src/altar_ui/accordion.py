from collections.abc import Generator, Iterable
from enum import StrEnum
from typing import Literal, Self

from aether import BaseWebElement
from aether.plugins.alpinejs import AlpineJSData, Statement, alpine_js_data_merge
from aether.plugins.tailwindcss import tw_merge
from aether.tags.html import (
    Button as PyButton,
)
from aether.tags.html import (
    ButtonAttributes as PyButtonAttributes,
)
from aether.tags.html import Div, DivAttributes
from altar_icons import ChevronDownIcon

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


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
            data_slot="accordion",
            **attributes,
        )


class AccordionItem(Div):
    def __init__(self, **attributes: Unpack[DivAttributes]):
        if attributes.get("id"):
            id_attribute = attributes.pop("id")
        elif attributes.get(":id"):
            id_attribute = attributes.pop(":id")
        else:
            id_attribute = "$id('accordion-item')"

        base_class_attribute = "border-b last:border-b-0"
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
            _class=tw_merge(class_attribute, base_class_attribute),
            x_data=alpine_js_data_merge(base_x_data_attribute, x_data_attribute),
            data_slot="accordion-item",
            **attributes,
        )


class AccordionTrigger(Div):
    def __init__(self, **attributes: Unpack[PyButtonAttributes]):
        self.forwarded_base_class_attribute = "flex flex-1 gap-4 justify-between items-start py-4 font-medium text-left text-sm rounded-md outline-none transition-all disabled:opacity-50 disabled:pointer-events-none hover:underline focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px]"
        self.forwarded_class_attribute = attributes.pop("_class", "")

        if attributes.get("id"):
            self.forwarded_id_attribute = attributes.pop("id")
        elif attributes.get(":id"):
            self.forwarded_id_attribute = attributes.pop(":id")
        else:
            self.forwarded_id_attribute = "$id('accordion-trigger')"

        self.forwarded_attributes = attributes

        super().__init__(_class="flex")

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
            PyButton(
                _class=tw_merge(
                    self.forwarded_class_attribute, self.forwarded_base_class_attribute
                ),
                data_slot="accordion-trigger",
                **{
                    "@click": "toggleActiveAccordionState(item_id)",
                    ":aria-controls": "item_id",
                    ":id": f"`${{item_id}}-${self.forwarded_id_attribute}`",
                },
                **self.forwarded_attributes,
            )(
                *forwarded_children,
                ChevronDownIcon(
                    _class="text-muted-foreground transition-transform duration-200 translate-y-0.5 pointer-events-none size-4 shrink-0",
                    **{":class": "{ 'rotate-180': isActive(item_id) }"},
                ),
            ),
        )

        return self


class AccordionContent(Div):
    def __init__(self, **attributes: Unpack[DivAttributes]):
        if attributes.get("id"):
            id_attribute = attributes.pop("id")
        elif attributes.get(":id"):
            id_attribute = attributes.pop(":id")
        else:
            id_attribute = "$id('accordion-content')"

        self.forwarded_base_class_attribute = "pt-0 pb-4"
        self.forwarded_class_attribute = attributes.pop("_class", "")
        self.forwarded_attributes = attributes

        super().__init__(
            _class="overflow-hidden text-sm",
            x_show="isActive(item_id)",
            x_cloak=True,
            x_collapse=True,
            role="region",
            data_slot="accordion-content",
            **{
                ":aria_labelledby": "item_id",
                ":id": f"`${{item_id}}-${id_attribute}`",
            },
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
            Div(
                _class=tw_merge(
                    self.forwarded_class_attribute, self.forwarded_base_class_attribute
                ),
                **self.forwarded_attributes,
            )(*forwarded_children)
        )

        return self
