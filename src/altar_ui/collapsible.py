from typing import Literal

from aether.plugins.alpinejs import AlpineJSData, Statement, alpine_js_data_merge
from aether.tags.html import (
    ButtonAttributes as PyButtonAttributes,
)
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
                    "{ if (this.isDisabled === false) { this.isOpen = !this.isOpen } }",
                    seq_type="definition",
                ),
            },
            directive="x-data",
        )
        x_data_attribute = attributes.pop("x_data", None)

        super().__init__(
            x_data=alpine_js_data_merge(base_x_data_attribute, x_data_attribute),
            data_slot="collapsible",
            **attributes,
        )


class CollapsibleTrigger(Button):
    def __init__(
        self,
        variant: Literal[
            "default", "destructive", "outline", "secondary", "ghost", "link"
        ] = "default",
        size: Literal["default", "sm", "lg", "icon"] = "default",
        **attributes: Unpack[PyButtonAttributes],
    ):
        super().__init__(
            type="button",
            variant=variant,
            size=size,
            data_slot="collapsible-trigger",
            **{
                "@click": "toggleCollapsibleState()",
                ":aria-expanded": "isOpen",
                ":disabled": "isDisabled",
            },
            **attributes,
        )


class CollapsibleContent(Div):
    def __init__(self, **attributes: Unpack[DivAttributes]):
        super().__init__(
            x_show="isOpen && ! isDisabled",
            data_slot="collapsible-content",
            **attributes,
        )
