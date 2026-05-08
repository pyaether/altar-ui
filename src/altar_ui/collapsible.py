"""Collapsible

An interactive component which expands/collapses a panel.

Composition:
    Use the following composition to build a Collapsible:

    Collapsible
    ├── CollapsibleTrigger
    └── CollapsibleContent
"""

from typing import Literal, Self

from aether.plugins.alpinejs import AlpineJSData, Statement, alpine_js_data_merge
from aether.plugins.tailwindcss import tw_merge
from aether.tags.html import ButtonAttributes as PyButtonAttributes
from aether.tags.html import Div, DivAttributes

from .button import Button

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack  # noqa: UP035


class Collapsible(Div):
    def __init__(
        self,
        default_open: bool = False,
        disabled: bool = False,
        **attributes: Unpack[DivAttributes],
    ):
        base_x_data_attribute = AlpineJSData(
            data={
                "isOpen": default_open,
                "isDisabled": disabled,
                "toggleCollapsibleState()": Statement(
                    "{ !this.isDisabled && (this.isOpen = !this.isOpen) }",
                    seq_type="definition",
                ),
            },
            directive="x-data",
        )
        x_data_attribute = attributes.pop("x_data", None)

        super().__init__(
            x_data=alpine_js_data_merge(base_x_data_attribute, x_data_attribute),
            **attributes,
        )


class CollapsibleTrigger(Button):
    def __init__(
        self,
        variant: Literal[
            "default", "destructive", "outline", "secondary", "ghost", "link"
        ] = "default",
        size: Literal["default", "sm", "lg", "icon", "icon_sm", "icon_lg"] = "icon",
        **attributes: Unpack[PyButtonAttributes],
    ):
        super().__init__(
            type="button",
            variant=variant,
            size=size,
            **{
                "@click": "toggleCollapsibleState()",
                ":aria-expanded": "isOpen",
                ":disabled": "isDisabled",
            },
            **attributes,
        )


class CollapsibleContent(Div):
    def __init__(self, **attributes: Unpack[DivAttributes]):
        base_class_attribute = (
            "grid transition-[grid-template-rows] duration-200 ease-in-out"
        )
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            x_show="isOpen && !isDisabled",
            **{
                ":class": "isOpen && !isDisabled ? 'grid-rows-[1fr]' : 'grid-rows-[0fr]'"
            },
            **attributes,
        )

    def __call__(self, *children: tuple) -> Self:
        self.children.append(Div(_class="overflow-hidden")(*children))
        return self
