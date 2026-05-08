"""Card

Displays a card with header, content, and footer.

Composition:
    Use the following composition to build a Card:

    Card
    ├── CardHeader
    │   ├── CardTitle
    │   ├── CardDescription
    │   └── CardAction
    ├── CardContent
    └── CardFooter
"""

from aether.plugins.tailwindcss import tw_merge
from aether.tags.html import (
    H2,
    Div,
    DivAttributes,
    Footer,
    FooterAttributes,
    HAttributes,
    Header,
    HeaderAttributes,
    P,
    PAttributes,
    Section,
    SectionAttributes,
)

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack  # noqa: UP035


class Card(Div):
    def __init__(self, **attributes: Unpack[DivAttributes]):
        base_class_attribute = "flex-col rounded-xl shadow-sm border text-card-foreground gap-6 flex bg-card py-6"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            **attributes,
        )


class CardHeader(Header):
    def __init__(self, **attributes: Unpack[HeaderAttributes]):
        base_class_attribute = "auto-rows-min grid-rows-[auto_auto] items-start grid gap-1.5 px-6 has-[[data-slot=card-action]]:grid-cols-[1fr_auto] [&.border-b]:pb-6 @container/card-header"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            **attributes,
        )


class CardTitle(H2):
    def __init__(self, **attributes: Unpack[HAttributes]):
        base_class_attribute = "leading-none font-semibold"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            **attributes,
        )


class CardDescription(P):
    def __init__(self, **attributes: Unpack[PAttributes]):
        base_class_attribute = "text-muted-foreground text-sm"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            **attributes,
        )


class CardAction(Div):
    def __init__(self, **attributes: Unpack[DivAttributes]):
        base_class_attribute = (
            "col-start-2 row-span-2 row-start-1 self-start justify-self-end"
        )
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            data_slot="card-action",
            **attributes,
        )


class CardContent(Section):
    def __init__(self, **attributes: Unpack[SectionAttributes]):
        base_class_attribute = "px-6"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            **attributes,
        )


class CardFooter(Footer):
    def __init__(self, **attributes: Unpack[FooterAttributes]):
        base_class_attribute = "items-center flex px-6 [&.border-t]:pt-6"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            **attributes,
        )
