"""Badge

Displays a badge or a component that looks like a badge.

Composition:
    Use the following composition to build a Badge:

    Badge
"""

from enum import StrEnum
from typing import Literal

from aether.plugins.tailwindcss import tw_merge
from aether.tags.html import Span, SpanAttributes

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack  # noqa: UP035


class BadgeVariant(StrEnum):
    default = "border-transparent bg-primary text-primary-foreground has-[>a]:hover:bg-primary/90"
    destructive = "border-transparent bg-destructive text-white has-[>a]:hover:bg-destructive/90 focus-visible:ring-destructive/20 dark:focus-visible:ring-destructive/40 dark:bg-destructive/60"
    outline = (
        "text-foreground has-[>a]:hover:bg-accent has-[>a]:hover:text-accent-foreground"
    )
    secondary = "border-transparent bg-secondary text-secondary-foreground has-[>a]:hover:bg-secondary/90"


class Badge(Span):
    def __init__(
        self,
        variant: Literal["default", "destructive", "outline", "secondary"] = "default",
        **attributes: Unpack[SpanAttributes],
    ):
        base_class_attribute = "whitespace-nowrap inline-flex transition-[color,box-shadow] overflow-hidden justify-center rounded-full border shrink-0 items-center font-medium text-xs gap-1 px-2 py-0.5 w-fit aria-invalid:border-destructive aria-invalid:ring-destructive/20 focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px] [&>svg]:pointer-events-none [&>svg]:size-3 dark:aria-invalid:ring-destructive/40"
        variant_class_attribute = BadgeVariant[variant]
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(
                variant_class_attribute, base_class_attribute, class_attribute
            ),
            **attributes,
        )
