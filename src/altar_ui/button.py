"""Button

Displays a button or a component that looks like a button.

Composition:
    Use the following composition to build a Button:

    Button
"""

from enum import StrEnum
from typing import Literal

from aether.plugins.tailwindcss import tw_merge
from aether.tags.html import Button as PyButton
from aether.tags.html import ButtonAttributes as PyButtonAttributes
from aether.tags.html import Div, DivAttributes

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack  # noqa: UP035


class ButtonGroupOrientation(StrEnum):
    horizontal = "[&>hr[role=separator]]:w-0 [&>hr[role=separator]]:h-auto [&>hr[role=separator]]:self-stretch [&>*:not(:first-child)]:rounded-l-none [&>*:not(:first-child)]:border-l-0 [&>:is(([data-slot=dropdown-menu],[data-slot=popover],[data-slot=select])):not(:first-child)>button]:rounded-l-none [&>:is(([data-slot=dropdown-menu],[data-slot=popover],[data-slot=select])):not(:first-child)>button]:border-l-0 [&>*:not(:last-child)]:rounded-r-none [&>:is(([data-slot=dropdown-menu],[data-slot=popover],[data-slot=select])):not(:last-child)>button]:rounded-r-none"
    vertical = "flex-col [&>hr[role=separator]]:w-auto [&>hr[role=separator]]:h-px [&>*:not(:first-child)]:rounded-t-none [&>*:not(:first-child)]:border-t-0 [&>:is(([data-slot=dropdown-menu],[data-slot=popover],[data-slot=select])):not(:first-child)>button]:rounded-t-none [&>:is(([data-slot=dropdown-menu],[data-slot=popover],[data-slot=select])):not(:first-child)>button]:border-t-0 [&>*:not(:last-child)]:rounded-b-none [&>:is(([data-slot=dropdown-menu],[data-slot=popover],[data-slot=select])):not(:last-child)>button]:rounded-b-none"


class ButtonVariant(StrEnum):
    default = "bg-primary text-primary-foreground shadow-xs hover:bg-primary/90 aria-[pressed=true]:bg-primary/90"
    destructive = "bg-destructive text-white shadow-xs focus-visible:ring-destructive/20 dark:focus-visible:ring-destructive/40 dark:bg-destructive/60 hover:bg-destructive/90 dark:hover:bg-destructive/50 aria-[pressed=true]:bg-destructive/90 dark:aria-[pressed=true]:bg-destructive/50"
    outline = "border bg-background shadow-xs dark:bg-input/30 dark:border-input hover:bg-accent hover:text-accent-foreground dark:hover:bg-accent/50 aria-[pressed=true]:bg-accent aria-[pressed=true]:text-accent-foreground dark:aria-[pressed=true]:bg-accent/50"
    secondary = "bg-secondary text-secondary-foreground shadow-xs hover:bg-secondary/80 aria-[pressed=true]:bg-secondary/80"
    ghost = "hover:bg-accent hover:text-accent-foreground dark:hover:bg-accent/50 aria-[pressed=true]:bg-accent aria-[pressed=true]:text-accent-foreground dark:aria-[pressed=true]:bg-accent/50"
    link = (
        "text-primary underline-offset-4 hover:underline aria-[pressed=true]:underline"
    )


class ButtonSize(StrEnum):
    default = "gap-2 h-9 px-4 py-2 has-[>svg]:px-3"
    sm = "gap-1.5 h-8 px-3 has-[>svg]:px-2.5"
    lg = "gap-2 h-10 px-6 has-[>svg]:px-4"
    icon = "size-9"
    icon_sm = "size-8"
    icon_lg = "size-10"


class ButtonGroup(Div):
    def __init__(
        self,
        orientation: Literal["horizontal", "vertical"] = "horizontal",
        **attributes: Unpack[DivAttributes],
    ):
        base_class_attribute = "inline-flex items-stretch w-fit [&>*:focus-visible]:relative [&>:is(([data-slot=dropdown-menu],[data-slot=popover],[data-slot=select]))>button:focus-visible]:relative [&>hr[role=separator]]:border-input [&>hr[role=separator]]:border [&>hr[role=separator]]:shrink-0 [&>*:focus-visible]:z-10 [&>:is(([data-slot=dropdown-menu],[data-slot=popover],[data-slot=select]))>button:focus-visible]:z-10 [&>hr[role=separator]]:m-0"
        orientation_class_attribute = ButtonGroupOrientation[orientation]

        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(
                orientation_class_attribute, base_class_attribute, class_attribute
            ),
            role="group",
            **attributes,
        )


class Button(PyButton):
    def __init__(
        self,
        variant: Literal[
            "default", "destructive", "outline", "secondary", "ghost", "link"
        ]
        | None = "default",
        size: Literal["default", "sm", "lg", "icon", "icon_sm", "icon_lg"] = "default",
        **attributes: Unpack[PyButtonAttributes],
    ):
        base_class_attribute = "outline-none whitespace-nowrap inline-flex transition-all justify-center rounded-md cursor-pointer shrink-0 items-center font-medium text-sm aria-invalid:border-destructive aria-invalid:ring-destructive/20 focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px] disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:shrink-0 [&_svg:not([class*='size-'])]:size-4 dark:aria-invalid:ring-destructive/40"
        size_class_attribute = ButtonSize[size]
        variant_class_attribute = ButtonVariant[variant] if variant is not None else ""

        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(
                variant_class_attribute,
                size_class_attribute,
                base_class_attribute,
                class_attribute,
            ),
            **attributes,
        )
