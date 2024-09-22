from typing import Any, Dict, Generator, Iterable, Self, Tuple

from pytempl import BaseWebElement
from pytempl.plugins.tailwindcss import tw_merge
from pytempl.tags import H3, Button, Div
from pytempl_icons import ChevronDownIcon


class Accordion(Div):
    pass


class AccordionItem(Div):
    def __init__(self, **attributes: Dict[str, Any]):
        base_class_attribute = "border-b"
        class_attribute = attributes.pop("_class", "")
        super().__init__(
            _class=tw_merge(class_attribute, base_class_attribute),
            x_data="{ isExpanded: false }",
            **attributes,
        )


class AccordionTrigger(H3):
    def __init__(self, value: str, **attributes: Dict[str, Any]):
        self.forwarded_base_class_attribute = "flex flex-1 items-center justify-between py-4 text-sm font-medium transition-all hover:underline"
        self.forwarded_class_attribute = attributes.pop("_class", "")
        self.forwarded_attributes = attributes
        self.value = value
        super().__init__(_class="flex")

    def __call__(self, *children: Tuple) -> Self:
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
            Button(
                _class=tw_merge(
                    self.forwarded_class_attribute, self.forwarded_base_class_attribute
                ),
                id=f"accordion-trigger-{self.value.lower().replace(' ', '-')}",
                aria_controls=f"accordion-item-{self.value.lower().replace(' ', '-')}",
                **{"@click": "isExpanded = ! isExpanded"},
                **self.forwarded_attributes,
            )(
                *forwarded_children,
                ChevronDownIcon(
                    _class="h-4 w-4 shrink-0 text-muted-foreground transition-transform duration-200",
                    **{":class": "isExpanded ? 'rotate-180' : ''"},
                ),
            ),
        )

        return self


class AccordionContent(Div):
    def __init__(self, value: str, **attributes: Dict[str, Any]):
        self.forwarded_base_class_attribute = "pb-4 pt-0"
        self.forwarded_class_attribute = attributes.pop("_class", "")
        super().__init__(
            x_cloak=True,
            x_show="isExpanded",
            id=f"accordion-item-{value.lower().replace(' ', '-')}",
            role="region",
            aria_labelledby=f"accordion-trigger-{value.lower().replace(' ', '-')}",
            x_collapse=True,
            _class="overflow-hidden text-sm",
            **attributes,
        )

    def __call__(self, *children: Tuple) -> Self:
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
                )
            )(*forwarded_children)
        )

        return self
