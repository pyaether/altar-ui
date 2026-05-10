"""Popover

Displays rich content in a portal, triggered by a button.

Composition:
    Use the following composition to build a Popover:

    Popover
    ├── PopoverTrigger
    └── PopoverContent

Requires:
    AlpineJS Focus Plugin (x-trap on PopoverContent)
"""

from enum import StrEnum
from typing import Literal

from aether.plugins.alpinejs import AlpineJSData, Statement, alpine_js_data_merge
from aether.plugins.tailwindcss import tw_merge
from aether.tags.html import ButtonAttributes as PyButtonAttributes
from aether.tags.html import Div, DivAttributes

from .button import Button

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack  # noqa: UP035


class PopoverContentPosition(StrEnum):
    top = "mb-1 bottom-full aria-hidden:translate-y-2"
    bottom = "mt-1 top-full aria-hidden:-translate-y-2"
    left = "mr-1 right-full aria-hidden:translate-x-2"
    right = "ml-1 left-full aria-hidden:-translate-x-2"


class Popover(Div):
    def __init__(self, **attributes: Unpack[DivAttributes]):
        base_x_data_attribute = AlpineJSData(
            data={
                "isOpen": False,
                "togglePopoverState()": Statement(
                    "{ this.isOpen ? this.closePopover(true) : this.openPopover(); }",
                    seq_type="definition",
                ),
                "openPopover()": Statement(
                    "{ this.isOpen = true; }", seq_type="definition"
                ),
                "closePopover(focusOnTrigger)": Statement(
                    "{ if (!this.isOpen) return; this.isOpen = false; if (focusOnTrigger) { this.$refs.trigger?.focus(); } }",
                    seq_type="definition",
                ),
            },
            directive="x-data",
        )
        base_class_attribute = "inline-flex relative"
        class_attribute = attributes.pop("_class", "")
        x_data_attribute = attributes.pop("x_data", None)

        data_slot_attribute = attributes.pop("data_slot", "popover")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            x_data=alpine_js_data_merge(base_x_data_attribute, x_data_attribute),
            data_slot=data_slot_attribute,
            **{
                "@keydown.escape": "closePopover(true)",
                "@click.outside": "closePopover(false)",
            },
            **attributes,
        )


class PopoverTrigger(Button):
    def __init__(
        self,
        variant: Literal[
            "default", "destructive", "outline", "secondary", "ghost", "link"
        ] = "default",
        size: Literal["default", "sm", "lg", "icon", "icon_sm", "icon_lg"] = "default",
        **attributes: Unpack[PyButtonAttributes],
    ):
        super().__init__(
            type="button",
            variant=variant,
            size=size,
            x_ref="trigger",
            **{"@click": "togglePopoverState()", ":aria-expanded": "isOpen"},
            **attributes,
        )


class PopoverContent(Div):
    def __init__(
        self,
        position: Literal["top", "bottom", "left", "right"],
        alignment: Literal["start", "center", "end"] = "start",
        **attributes: Unpack[DivAttributes],
    ):
        variant_class_attribute = PopoverContentPosition[position]

        if position in ("top", "bottom"):
            match alignment:
                case "start":
                    variant_class_attribute += " left-0"
                case "center":
                    variant_class_attribute += " left-1/2 -translate-x-1/2"
                case "end":
                    variant_class_attribute += " right-0"
        elif position in ("left", "right"):
            match alignment:
                case "start":
                    variant_class_attribute += " top-0"
                case "center":
                    variant_class_attribute += " top-1/2 -translate-y-1/2"
                case "end":
                    variant_class_attribute += " bottom-0"

        base_class_attribute = "transition-all overflow-x-hidden overflow-y-auto absolute rounded-md shadow-md border min-w-full text-popover-foreground bg-popover w-max z-50 p-4"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(
                variant_class_attribute, base_class_attribute, class_attribute
            ),
            x_show="isOpen",
            x_cloak=True,
            x_trap="isOpen",
            **{
                ":class": "{ 'invisible opacity-0 scale-95': !isOpen, 'visible opacity-100 scale-100': isOpen }",
                "x-transition:leave": "transition ease-in duration-75",
                "x-transition:leave-start": "opacity-100 scale-100",
                "x-transition:leave-end": "opacity-0 scale-95",
            },
            **attributes,
        )
