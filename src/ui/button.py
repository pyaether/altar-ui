from enum import Enum
from typing import Any, Dict, Literal

from pytempl import html_class_merge
from pytempl.tags import Button as PyButton


class ButtonVariant(Enum):
    default = "bg-primary text-primary-foreground shadow hover:bg-primary/90"
    destructive = (
        "bg-destructive text-destructive-foreground shadow-sm hover:bg-destructive/90"
    )
    outline = "border border-input bg-background shadow-sm hover:bg-accent hover:text-accent-foreground"
    secondary = "bg-secondary text-secondary-foreground shadow-sm hover:bg-secondary/80"
    ghost = "hover:bg-accent hover:text-accent-foreground"
    link = "text-primary underline-offset-4 hover:underline"


class ButtonSize(Enum):
    default = "h-9 px-4 py-2"
    sm = "h-8 rounded-md px-3 text-xs"
    lg = "h-10 rounded-md px-8"
    icon = "h-9 w-9"


class Button(PyButton):
    def __init__(
        self,
        variant: Literal[
            "default", "destructive", "outline", "secondary", "ghost", "link"
        ] = "default",
        size: Literal["default", "sm", "lg", "icon"] = "default",
        **attributes: Dict[str, Any],
    ):
        base_class_attribute = "inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50"
        class_attribute = attributes.pop("_class", "")
        variant_class_attribute = ButtonVariant[variant]
        size_class_attribute = ButtonSize[size]

        super().__init__(
            _class=html_class_merge(
                class_attribute,
                f"{variant_class_attribute.value} {size_class_attribute.value} {base_class_attribute}",
            ),
            **attributes,
        )
