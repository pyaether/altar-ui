from enum import Enum
from typing import Any, Dict, Literal

from pytempl.plugins.tailwindcss import tw_merge
from pytempl.tags.html import H3, Div, Li, Ul

from .button import Button


class PopoverSide(Enum):
    bottom = "slide-in-from-top-2"
    top = "slide-in-from-bottom-2"
    left = "slide-in-from-right-2"
    right = "slide-in-from-left-2"


class DropdownMenu(Div):
    def __init__(self, **attributes: Dict[str, Any]):
        super().__init__(
            x_data="{ isOpened: false, openedWithKeyboard: false }",
            **{"@keydown.esc.window": "isOpened = false, openedWithKeyboard = false"},
            **attributes,
        )


class DropdownMenuTrigger(Button):
    def __init__(
        self,
        variant: Literal[
            "default", "destructive", "outline", "secondary", "ghost", "link"
        ] = "default",
        size: Literal["default", "sm", "lg", "icon"] = "default",
        **attributes: Dict[str, Any],
    ):
        super().__init__(
            type="button",
            variant=variant,
            size=size,
            aria_haspopup="true",
            **{
                "@click": "isOpened = ! isOpened",
                ":aria-expanded": "isOpened || openedWithKeyboard",
                "@keydown.space.prevent": "openedWithKeyboard = true",
                "@keydown.enter.prevent": "openedWithKeyboard = true",
                "@keydown.down.prevent": "openedWithKeyboard = true",
            },
            **attributes,
        )


class DropdownMenuContent(Ul):
    def __init__(
        self,
        popover_side: Literal["bottom", "top", "left", "right"] = "bottom",
        **attributes: Dict[str, Any],
    ):
        base_class_attribute = "z-50 min-w-[8rem] overflow-hidden rounded-md border bg-popover p-1 text-popover-foreground shadow-md"
        class_attribute = attributes.pop("_class", "")
        popover_side_class_attribute = PopoverSide[popover_side]

        super().__init__(
            x_cloak=True,
            x_show="isOpened || openedWithKeyboard",
            x_trap="openedWithKeyboard",
            role="menu",
            _class=tw_merge(
                class_attribute,
                f"{class_attribute} {base_class_attribute} {popover_side_class_attribute.value}",
            ),
            **{
                ":class": "(isOpened || openedWithKeyboard) ? 'animate-in fade-in-0 zoom-in-95' : 'animate-out fade-out-0 zoom-out-95'",
                "@click.outside": "isOpened = false, openedWithKeyboard = false",
                "@keydown.down.prevent": "$focus.wrap().next()",
                "@keydown.up.prevent": "$focus.wrap().previous()",
            },
            **attributes,
        )


class DropdownMenuLabel(H3):
    def __init__(self, inset: bool = False, **attributes: Dict[str, Any]):
        base_class_attribute = "px-2 py-1.5 text-sm font-semibold"
        class_attribute = attributes.pop("_class", "")
        inset_class_attribute = "pl-8" if inset else ""

        super().__init__(
            _class=tw_merge(
                class_attribute, f"{base_class_attribute} {inset_class_attribute}"
            ),
            **attributes,
        )


class DropdownMenuItem(Li):
    def __init__(
        self, inset: bool = False, disabled: bool = False, **attributes: Dict[str, Any]
    ):
        base_class_attribute = "relative flex cursor-default select-none items-center rounded-sm px-2 py-1.5 text-sm outline-none transition-colors focus:bg-accent focus:text-accent-foreground"
        class_attribute = attributes.pop("_class", "")
        inset_class_attribute = "pl-8" if inset else ""
        disabled_class_attribute = "pointer-events-none opacity-50" if disabled else ""

        super().__init__(
            _class=tw_merge(
                class_attribute,
                f"{base_class_attribute} {inset_class_attribute} {disabled_class_attribute}",
            ),
            role="menuitem",
            **attributes,
        )


class DropdownMenuSeparator(Div):
    have_children = False

    def __init__(self, **attributes: Dict[str, Any]):
        base_class_attribute = "-mx-1 my-1 h-px bg-muted"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(class_attribute, base_class_attribute),
            role="separator",
            aria_orientation="horizontal",
            **attributes,
        )


# To add: DropdownMenuShortcut, DropdownMenuSub, DropdownMenuSubContent, DropdownMenuSubTrigger, DropdownMenuPortal, DropdownMenuCheckboxItem, DropdownMenuRadioItem, DropdownMenuGroup, DropdownMenuRadioGroup
