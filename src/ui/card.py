from pytempl.plugins.tailwindcss import tw_merge
from pytempl.tags.html import H3, Div, DivAttributes, HAttributes, P, PAttributes

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class Card(Div):
    def __init__(self, **attributes: Unpack[DivAttributes]):
        base_class_attribute = "rounded-xl border bg-card text-card-foreground shadow"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(class_attribute, base_class_attribute), **attributes
        )


class CardHeader(Div):
    def __init__(self, **attributes: Unpack[DivAttributes]):
        base_class_attribute = "flex flex-col space-y-1.5 p-6"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(class_attribute, base_class_attribute), **attributes
        )


class CardContent(Div):
    def __init__(self, **attributes: Unpack[DivAttributes]):
        base_class_attribute = "p-6 pt-0"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(class_attribute, base_class_attribute), **attributes
        )


class CardTitle(H3):
    def __init__(self, **attributes: Unpack[HAttributes]):
        base_class_attribute = "font-semibold leading-none tracking-tight"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(class_attribute, base_class_attribute), **attributes
        )


class CardDescription(P):
    def __init__(self, **attributes: Unpack[PAttributes]):
        base_class_attribute = "text-sm text-muted-foreground"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(class_attribute, base_class_attribute), **attributes
        )


class CardFooter(Div):
    def __init__(self, **attributes: Unpack[DivAttributes]):
        base_class_attribute = "flex items-center p-6 pt-0"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(class_attribute, base_class_attribute), **attributes
        )
