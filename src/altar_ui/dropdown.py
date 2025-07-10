import warnings
from typing import Literal, Self

from aether.plugins.alpinejs import AlpineJSData, Statement, alpine_js_data_merge
from aether.plugins.tailwindcss import tw_merge
from aether.tags.html import (
    ButtonAttributes as PyButtonAttributes,
)
from aether.tags.html import Div, DivAttributes

from .button import Button

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack  # noqa: UP035


class DropdownMenu(Div):
    def __init__(self, **attributes: Unpack[DivAttributes]):
        base_x_data_attribute = AlpineJSData(
            data={
                "isOpen": False,
                "toggleDropdownMenu()": Statement(
                    content="{ this.isOpen = !this.isOpen }", seq_type="definition"
                ),
            },
            directive="x-data",
        )
        x_data_attribute = attributes.pop("x_data", None)

        super().__init__(
            x_data=alpine_js_data_merge(base_x_data_attribute, x_data_attribute),
            **{"@keydown.escape.window": "isOpen = false"},
            **attributes,
        )


class DropdownMenuTrigger(Button):
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
            aria_haspopup="true",
            x_ref="dropdownMenuTrigger",
            data_slot="dropdown-menu-trigger",
            **{
                "@click": "toggleDropdownMenu()",
                ":aria-expanded": "isOpen",
                "@keydown.space.prevent": "toggleDropdownMenu()",
                "@keydown.enter.prevent": "toggleDropdownMenu()",
            },
            **attributes,
        )


class DropdownMenuContent(Div):
    def __init__(
        self,
        side_position: Literal["bottom", "top", "left", "right"] = "bottom",
        side_align: Literal["start", "end"] = "start",
        side_offset: int = 8,
        **attributes: Unpack[DivAttributes],
    ):
        base_class_attribute = "overflow-x-hidden overflow-y-auto z-50 p-1 min-w-[8rem] max-h-[18rem] text-popover-foreground bg-popover rounded-md border shadow-md"
        data_side_class_attribute = "data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            x_cloak=True,
            x_show="isOpen",
            x_trap="isOpen",
            role="menu",
            data_side=side_position,
            data_slot="dropdown-menu-content",
            _class=tw_merge(
                class_attribute, f"{base_class_attribute} {data_side_class_attribute}"
            ),
            **{
                "@click.outside": "isOpen = false",
                "@keydown.down.prevent": "$focus.wrap().next()",
                "@keydown.up.prevent": "$focus.wrap().previous()",
                "x-transition:leave": "animate-out zoom-out-95 fade-out-0",
                "x-transition:enter": "animate-in zoom-in-95 fade-in-0",
                f"x-anchor.{side_position}-{side_align}.offset.{side_offset}": "$refs.dropdownMenuTrigger",
            },
            **attributes,
        )


class DropdownMenuGroup(Div):
    def __init__(self, **attributes: Unpack[DivAttributes]):
        super().__init__(data_slot="dropdown-menu-group", **attributes)


class DropdownMenuItem(Div):
    def __init__(
        self,
        disabled: bool = False,
        inset: bool = False,
        variant: Literal["default", "destructive"] = "default",
        **attributes: Unpack[DivAttributes],
    ):
        base_class_attribute = "flex relative gap-2 items-center px-2 py-1.5 text-sm rounded-sm outline-hidden cursor-default select-none [&_svg:not([class*='text-'])]:text-muted-foreground [&_svg:not([class*='size-'])]:size-4 hover:text-accent-foreground hover:bg-accent focus:text-accent-foreground focus:bg-accent [&_svg]:pointer-events-none [&_svg]:shrink-0"
        data_disabled_class_attribute = (
            "data-[disabled]:pointer-events-none data-[disabled]:opacity-50"
        )
        data_inset_class_attribute = "data-[inset]:pl-8"
        data_variant_class_attribute = "data-[variant=destructive]:text-destructive data-[variant=destructive]:focus:bg-destructive/10 data-[variant=destructive]:focus:text-destructive data-[variant=destructive]:*:[svg]:!text-destructive dark:data-[variant=destructive]:focus:bg-destructive/20"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(
                class_attribute,
                f"{base_class_attribute} {data_disabled_class_attribute} {data_inset_class_attribute} {data_variant_class_attribute}",
            ),
            role="menuitem",
            data_disabled=disabled,
            data_inset=inset,
            data_variant=variant,
            data_slot="dropdown-menu-item",
            **attributes,
        )


class DropdownMenuLabel(Div):
    def __init__(self, inset: bool = False, **attributes: Unpack[DivAttributes]):
        base_class_attribute = "px-2 py-1.5 font-medium text-sm"
        data_inset_class_attribute = "data-[inset]:pl-8"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(
                class_attribute, f"{base_class_attribute} {data_inset_class_attribute}"
            ),
            data_inset=inset,
            data_slot="dropdown-menu-label",
            **attributes,
        )


class DropdownMenuSeparator(Div):
    def __init__(self, **attributes: Unpack[DivAttributes]):
        base_class_attribute = "my-1 h-px bg-border -mx-1"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(class_attribute, base_class_attribute),
            role="separator",
            aria_orientation="horizontal",
            data_slot="dropdown-menu-separator",
            **attributes,
        )

    def __call__(self, *_children: tuple) -> Self:
        warnings.warn(
            f"Trying to add child to a non-child element: {self.__class__.__qualname__}",
            UserWarning,
            stacklevel=2,
        )
        return self


# To add: DropdownMenuShortcut, DropdownMenuSub, DropdownMenuSubContent, DropdownMenuSubTrigger, DropdownMenuCheckboxItem, DropdownMenuRadioItem, DropdownMenuRadioGroup
