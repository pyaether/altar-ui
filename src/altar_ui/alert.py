"""Alert

Displays a callout for user attention.

Composition:
    Use the following composition to build an Alert:

    Alert
    ├── AlertTitle
    └── AlertDescription
"""

from enum import StrEnum
from typing import Literal

from aether.plugins.tailwindcss import tw_merge
from aether.tags.html import (
    H5,
    Div,
    DivAttributes,
    HAttributes,
    Section,
    SectionAttributes,
)

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack  # noqa: UP035


class AlertVariant(StrEnum):
    default = "bg-card text-card-foreground"
    destructive = "text-destructive bg-card [&>svg]:text-current"


class AlertDescriptionVariant(StrEnum):
    default = "text-muted-foreground"
    destructive = "text-destructive"


class Alert(Div):
    def __init__(
        self,
        variant: Literal["default", "destructive"] = "default",
        **attributes: Unpack[DivAttributes],
    ):
        base_class_attribute = "grid-cols-[0_1fr] relative rounded-lg border items-start text-sm grid gap-y-0.5 px-4 py-3 w-full has-[>svg]:grid-cols-[calc(var(--spacing)*4)_1fr] has-[>svg]:gap-x-3 [&>svg]:translate-y-0.5 [&>svg]:text-current [&>svg]:size-4"
        variant_class_attribute = AlertVariant[variant]
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(
                variant_class_attribute, base_class_attribute, class_attribute
            ),
            role="alert",
            **attributes,
        )


class AlertTitle(H5):
    def __init__(self, **attributes: Unpack[HAttributes]):
        base_class_attribute = (
            "col-start-2 line-clamp-1 min-h-4 font-medium tracking-tight"
        )
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            **attributes,
        )


class AlertDescription(Section):
    def __init__(
        self,
        variant: Literal["default", "destructive"] = "default",
        **attributes: Unpack[SectionAttributes],
    ):
        variant_class_attribute = AlertDescriptionVariant[variant]
        base_class_attribute = "justify-items-start text-sm grid col-start-2 gap-1 [&_p]:leading-relaxed [&_ul]:text-sm [&_ul]:list-inside [&_ul]:list-disc"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(
                variant_class_attribute, base_class_attribute, class_attribute
            ),
            **attributes,
        )
