from collections.abc import Generator, Iterable
from enum import StrEnum
from typing import Literal, Self

from aether import BaseWebElement
from aether.plugins.tailwindcss import tw_merge
from aether.tags.html import Div, DivAttributes, P

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack  # noqa: UP035


class AlertVariant(StrEnum):
    default = "bg-card text-card-foreground"
    destructive = "text-destructive bg-card [&>svg]:text-current *:data-[slot=alert-description]:text-destructive/90"


class Alert(Div):
    def __init__(
        self,
        variant: Literal["default", "destructive"] = "default",
        **attributes: Unpack[DivAttributes],
    ):
        base_class_attribute = "grid grid-cols-[0_1fr] relative gap-y-0.5 items-start px-4 py-3 w-full text-sm rounded-lg border has-[>svg]:grid-cols-[calc(var(--spacing)*4)_1fr] has-[>svg]:gap-x-3 [&>svg]:text-current [&>svg]:translate-y-0.5 [&>svg]:size-4"
        variant_class_attribute = AlertVariant[variant]
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(
                class_attribute,
                f"{variant_class_attribute} {base_class_attribute}",
            ),
            data_slot="alert",
            role="alert",
            **attributes,
        )


class AlertTitle(Div):
    def __init__(self, **attributes: Unpack[DivAttributes]):
        base_class_attribute = (
            "col-start-2 line-clamp-1 min-h-4 font-medium tracking-tight"
        )
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(class_attribute, base_class_attribute),
            data_slot="alert-title",
            **attributes,
        )


class AlertDescription(Div):
    def __init__(self, **attributes: Unpack[DivAttributes]):
        base_class_attribute = "grid gap-1 justify-items-start text-muted-foreground text-sm col-start-2 [&_ol]:ml-4 [&_ul]:ml-4 [&_p]:leading-relaxed"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(class_attribute, base_class_attribute), **attributes
        )

    def __call__(self, *children: tuple) -> Self:
        for child in children:
            if (
                isinstance(child, str)
                or isinstance(child, BaseWebElement)
                or not isinstance(child, Iterable)
            ):
                if isinstance(child, str):
                    self.children.append(P()(child))
                else:
                    self.children.append(child)
            elif isinstance(child, Generator):
                self.children.extend(list(child))
            elif isinstance(child, type(None)):
                continue
            else:
                self.children.extend(child)

        return self
