from enum import Enum
from typing import Any, Dict, Literal

from pytempl.plugins.tailwindcss import tw_merge
from pytempl.tags.html import Div


class BadgeVariant(Enum):
    default = "border-transparent bg-primary text-primary-foreground shadow hover:bg-primary/80"
    destructive = "border-transparent bg-destructive text-destructive-foreground shadow hover:bg-destructive/80"
    outline = "text-foreground"
    secondary = "border-transparent bg-secondary text-secondary-foreground hover:bg-secondary/80"


class Badge(Div):
    def __init__(
        self,
        variant: Literal["default", "destructive", "outline", "secondary"] = "default",
        **attributes: Dict[str, Any],
    ):
        base_class_attribute = "inline-flex items-center rounded-md border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
        class_attribute = attributes.pop("_class", "")
        variant_class_attribute = BadgeVariant[variant]

        super().__init__(
            _class=tw_merge(
                class_attribute,
                f"{variant_class_attribute.value} {base_class_attribute}",
            ),
            **attributes,
        )
