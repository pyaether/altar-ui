from aether.plugins.tailwindcss import tw_merge
from aether.tags.html import Div, DivAttributes

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack  # noqa: UP035


class Card(Div):
    def __init__(self, **attributes: Unpack[DivAttributes]):
        base_class_attribute = "flex flex-col gap-6 py-6 text-card-foreground bg-card rounded-xl border shadow-sm"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(class_attribute, base_class_attribute),
            data_slot="card",
            **attributes,
        )


class CardHeader(Div):
    def __init__(self, **attributes: Unpack[DivAttributes]):
        base_class_attribute = "grid grid-rows-[auto_auto] gap-1.5 items-start px-6 @container/card-header auto-rows-min has-data-[slot=card-action]:grid-cols-[1fr_auto] [.border-b]:pb-6"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(class_attribute, base_class_attribute),
            data_slot="card-header",
            **attributes,
        )


class CardTitle(Div):
    def __init__(self, **attributes: Unpack[DivAttributes]):
        base_class_attribute = "font-semibold leading-none"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(class_attribute, base_class_attribute),
            data_slot="card-title",
            **attributes,
        )


class CardDescription(Div):
    def __init__(self, **attributes: Unpack[DivAttributes]):
        base_class_attribute = "text-muted-foreground text-sm"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(class_attribute, base_class_attribute),
            data_slot="card-description",
            **attributes,
        )


class CardAction(Div):
    def __init__(self, **attributes: Unpack[DivAttributes]):
        base_class_attribute = (
            "col-start-2 row-span-2 row-start-1 self-start justify-self-end"
        )
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(class_attribute, base_class_attribute),
            data_slot="card-action",
            **attributes,
        )


class CardContent(Div):
    def __init__(self, **attributes: Unpack[DivAttributes]):
        base_class_attribute = "px-6"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(class_attribute, base_class_attribute),
            data_slot="card-content",
            **attributes,
        )


class CardFooter(Div):
    def __init__(self, **attributes: Unpack[DivAttributes]):
        base_class_attribute = "flex items-center px-6 [.border-t]:pt-6"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(class_attribute, base_class_attribute),
            data_slot="card-footer",
            **attributes,
        )
