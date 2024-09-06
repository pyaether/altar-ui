from enum import Enum
from typing import Any, Dict, Generator, Iterable, Literal, Self, Tuple

from pytempl import BaseWebElement, tw_merge
from pytempl.tags import H5, Div, P


class AlertVariant(Enum):
    default = "bg-background text-foreground"
    destructive = "border-destructive/50 text-destructive dark:border-destructive [&>svg]:text-destructive"


class Alert(Div):
    def __init__(
        self,
        variant: Literal["default", "destructive"] = "default",
        **attributes: Dict[str, Any],
    ):
        base_class_attribute = "relative w-full rounded-lg border px-4 py-3 text-sm [&>svg+div]:translate-y-[-3px] [&>svg]:absolute [&>svg]:left-4 [&>svg]:top-4 [&>svg]:text-foreground [&>svg~*]:pl-7"
        class_attribute = attributes.pop("_class", "")
        variant_class_attribute = AlertVariant[variant]

        super().__init__(
            _class=tw_merge(
                class_attribute,
                f"{variant_class_attribute.value} {base_class_attribute}",
            ),
            role="alert",
            **attributes,
        )


class AlertTitle(H5):
    def __init__(self, **attributes):
        base_class_attribute = "mb-1 font-medium leading-none tracking-tight"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(class_attribute, base_class_attribute), **attributes
        )


class AlertDescription(Div):
    def __init__(self, **attributes):
        base_class_attribute = "text-sm [&_p]:leading-relaxed [&_ol]:ml-4 [&_ul]:ml-4"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(class_attribute, base_class_attribute), **attributes
        )

    def __call__(self, *children: Tuple) -> Self:
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
