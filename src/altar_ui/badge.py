from enum import StrEnum
from typing import Literal

from aether.plugins.tailwindcss import tw_merge
from aether.tags.html import Span, SpanAttributes

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class BadgeVariant(StrEnum):
    default = (
        "border-transparent bg-primary text-primary-foreground [a&]:hover:bg-primary/90"
    )
    destructive = "border-transparent bg-destructive text-white [a&]:hover:bg-destructive/90 focus-visible:ring-destructive/20 dark:focus-visible:ring-destructive/40 dark:bg-destructive/60"
    outline = "text-foreground [a&]:hover:bg-accent [a&]:hover:text-accent-foreground"
    secondary = "border-transparent bg-secondary text-secondary-foreground [a&]:hover:bg-secondary/90"


class Badge(Span):
    def __init__(
        self,
        variant: Literal["default", "destructive", "outline", "secondary"] = "default",
        **attributes: Unpack[SpanAttributes],
    ):
        base_class_attribute = "inline-flex items-center justify-center rounded-md border px-2 py-0.5 text-xs font-medium w-fit whitespace-nowrap shrink-0 [&>svg]:size-3 gap-1 [&>svg]:pointer-events-none focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px] aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 aria-invalid:border-destructive transition-[color,box-shadow] overflow-hidden"
        variant_class_attribute = BadgeVariant[variant]
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(
                class_attribute,
                f"{variant_class_attribute} {base_class_attribute}",
            ),
            data_slot="badge",
            **attributes,
        )
