"""Tooltip

A popup that displays information related to an element when the element receives keyboard focus or the mouse hovers over it.

Composition:
    Use the following composition to build a Tooltip:

    Tooltip
"""

from enum import StrEnum
from typing import Literal

from aether.plugins.tailwindcss import tw_merge
from aether.tags.html import Div, DivAttributes

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack  # noqa: UP035


class TooltipPosition(StrEnum):
    top = "before:bottom-full before:mb-1.5 before:translate-y-2 hover:before:translate-y-0"
    bottom = (
        "before:top-full before:mt-1.5 before:-translate-y-2 hover:before:translate-y-0"
    )
    left = "before:right-full before:mr-1.5 before:translate-x-2 hover:before:translate-x-0"
    right = "before:left-full before:ml-1.5 before:-translate-x-2 hover:before:translate-x-0"


class Tooltip(Div):
    def __init__(
        self,
        text: str,
        position: Literal["top", "bottom", "left", "right"] = "top",
        alignment: Literal["start", "center", "end"] = "center",
        **attributes: Unpack[DivAttributes],
    ):
        variant_class_attribute = TooltipPosition[position]

        if position in ("top", "bottom"):
            match alignment:
                case "start":
                    variant_class_attribute += " before:left-0"
                case "center":
                    variant_class_attribute += (
                        " before:left-1/2 before:-translate-x-1/2"
                    )
                case "end":
                    variant_class_attribute += " before:right-0"
        elif position in ("left", "right"):
            match alignment:
                case "start":
                    variant_class_attribute += " before:top-0"
                case "center":
                    variant_class_attribute += " before:top-1/2 before:-translate-y-1/2"
                case "end":
                    variant_class_attribute += " before:bottom-0"

        base_class_attribute = "relative before:pointer-events-none before:transition-all before:invisible before:absolute before:opacity-0 before:truncate before:rounded-md before:content-[attr(data-tooltip)] before:scale-95 before:max-w-xs before:text-background before:text-xs before:px-3 before:bg-foreground before:py-1.5 before:w-fit before:z- hover:before:opacity-100 hover:before:visible hover:before:scale-100 [&:focus-visible:not(:hover)]:before:hidden"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(
                variant_class_attribute, base_class_attribute, class_attribute
            ),
            data_tooltip=text,
            **attributes,
        )
