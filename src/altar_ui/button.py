from enum import StrEnum
from typing import Literal

from aether.plugins.tailwindcss import tw_merge
from aether.tags.html import Button as PyButton
from aether.tags.html import ButtonAttributes as PyButtonAttributes

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack  # noqa: UP035


class ButtonVariant(StrEnum):
    default = "bg-primary text-primary-foreground shadow-xs hover:bg-primary/90"
    destructive = "bg-destructive text-white shadow-xs hover:bg-destructive/90 focus-visible:ring-destructive/20 dark:focus-visible:ring-destructive/40 dark:bg-destructive/60"
    outline = "border bg-background shadow-xs hover:bg-accent hover:text-accent-foreground dark:bg-input/30 dark:border-input dark:hover:bg-input/50"
    secondary = "bg-secondary text-secondary-foreground shadow-xs hover:bg-secondary/80"
    ghost = "hover:bg-accent hover:text-accent-foreground dark:hover:bg-accent/50"
    link = "text-primary underline-offset-4 hover:underline"


class ButtonSize(StrEnum):
    default = "h-9 px-4 py-2 has-[>svg]:px-3"
    sm = "h-8 rounded-md gap-1.5 px-3 has-[>svg]:px-2.5"
    lg = "h-10 rounded-md px-6 has-[>svg]:px-4"
    icon = "size-9"


class Button(PyButton):
    def __init__(
        self,
        variant: Literal[
            "default", "destructive", "outline", "secondary", "ghost", "link"
        ]
        | None = "default",
        size: Literal["default", "sm", "lg", "icon"] = "default",
        **attributes: Unpack[PyButtonAttributes],
    ):
        base_class_attribute = "inline-flex gap-2 justify-center items-center font-medium text-sm whitespace-nowrap rounded-md outline-none transition-all [&_svg:not([class*='size-'])]:size-4 shrink-0 aria-invalid:ring-destructive/20 aria-invalid:border-destructive dark:aria-invalid:ring-destructive/40 disabled:opacity-50 disabled:pointer-events-none focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px] [&_svg]:pointer-events-none [&_svg]:shrink-0"
        if variant is None:
            variant_class_attribute = ""
        else:
            variant_class_attribute = ButtonVariant[variant]
        size_class_attribute = ButtonSize[size]
        class_attribute = attributes.pop("_class", "")

        data_slot = attributes.pop("data_slot", "button")

        super().__init__(
            _class=tw_merge(
                class_attribute,
                f"{variant_class_attribute} {size_class_attribute} {base_class_attribute}",
            ),
            data_slot=data_slot,
            **attributes,
        )
