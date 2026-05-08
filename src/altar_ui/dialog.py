"""Dialog

A window overlaid on either the primary window or another dialog window, rendering the content underneath inert.

Composition:
    Use the following composition to build a Dialog:

    Dialog
    ├── DialogTrigger
    └── DialogContent
        ├── DialogHeader
        │   ├── DialogTitle
        │   └── DialogDescription
        ├── DialogBody
        └── DialogFooter

Requires:
    AlpineJS Focus Plugin (x-trap on DialogContent)
"""

from collections.abc import Generator, Iterable
from typing import Literal, Self

from aether import BaseWebElement
from aether.plugins.alpinejs import AlpineJSData, alpine_js_data_merge
from aether.plugins.tailwindcss import tw_merge
from aether.tags.html import (
    H2,
    Div,
    DivAttributes,
    HAttributes,
    P,
    PAttributes,
    Section,
    SectionAttributes,
    Span,
)
from aether.tags.html import Button as PyButton
from aether.tags.html import ButtonAttributes as PyButtonAttributes
from aether.tags.html import Dialog as PyDialog
from aether.tags.html import DialogAttributes as PyDialogAttributes
from altar_icons import XIcon

from .button import Button

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack  # noqa: UP035


class Dialog(Div):
    def __init__(self, **attributes: Unpack[DivAttributes]):
        base_x_data_attribute = AlpineJSData(data={"modalIsOpen": False})
        x_data_attribute = attributes.pop("x_data", None)

        super().__init__(
            x_data=alpine_js_data_merge(base_x_data_attribute, x_data_attribute),
            **attributes,
        )


class DialogTrigger(Button):
    def __init__(
        self,
        variant: Literal[
            "default", "destructive", "outline", "secondary", "ghost", "link"
        ] = "outline",
        size: Literal["default", "sm", "lg", "icon", "icon_sm", "icon_lg"] = "default",
        **attributes: Unpack[PyButtonAttributes],
    ):
        super().__init__(
            type="button",
            variant=variant,
            size=size,
            **{"@click": "modalIsOpen = true; $refs.dialog.showModal()"},
            **attributes,
        )


class DialogClose(PyButton):
    def __init__(self, **attributes: Unpack[PyButtonAttributes]):
        base_class_attribute = "transition-opacity opacity-70 rounded-xs ring-offset-background data-[state=open]:text-muted-foreground data-[state=open]:bg-accent hover:opacity-100 focus:outline-hidden focus:ring-ring focus:ring-2 focus:ring-offset-2 disabled:pointer-events-none [&_svg]:pointer-events-none [&_svg]:shrink-0[&_svg:not([class*='size-'])]:size-4"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            type="button",
            _class=tw_merge(base_class_attribute, class_attribute),
            **{
                "@click": "$dispatch('reset-form-data'); modalIsOpen = false; $refs.dialog.close()"
            },
            **attributes,
        )


class DialogContent(PyDialog):
    def __init__(self, **attributes: Unpack[PyDialogAttributes]):
        base_class_attribute = "transition-all transition-discrete opacity-0 inset-y-0 open:opacity-100 backdrop:transition-all backdrop:transition-discrete backdrop:opacity-0 backdrop:bg-black/50 [&:popover-open]:opacity-100 starting:open:opacity-0 open:backdrop:opacity-100 starting:[&:popover-open]:opacity-0 [&:popover-open]:backdrop:opacity-100 starting:open:backdrop:opacity-0 starting:[&:popover-open]:backdrop:opacity-0"

        self.forwarded_base_class_attribute = "transition-all flex-col rounded-lg shadow-lg scale-95 border max-w-[calc(100%-2rem)] max-h-[calc(100%-2rem)] left-[50%] fixed gap-4 top-[50%] flex bg-background w-full z-50 p-6 -translate-x-1/2 -translate-y-1/2 sm:max-w-lg [[open]>_&]:scale-100 [[:popover-open]>_&]:scale-100 starting:[[open]>_&]:scale-95 starting:[[:popover-open]>_&]:scale-95"
        self.forwarded_class_attribute = attributes.pop("_class", "")
        self.forwarded_attributes = attributes

        super().__init__(
            x_ref="dialog",
            _class=base_class_attribute,
            **{
                "x-trap.noscroll": "modalIsOpen",
                "@click": "$event.target === $el && (modalIsOpen = false, $el.close())",
                "@close": "modalIsOpen = false",
            },
        )

    def __call__(self, *children: tuple) -> Self:
        forwarded_children = []
        for child in children:
            if (
                isinstance(child, str)
                or isinstance(child, BaseWebElement)
                or not isinstance(child, Iterable)
            ):
                forwarded_children.append(child)
            elif isinstance(child, Generator):
                forwarded_children.extend(list(child))
            elif isinstance(child, type(None)):
                continue
            else:
                forwarded_children.extend(child)

        self.children.append(
            Div(
                _class=tw_merge(
                    self.forwarded_base_class_attribute, self.forwarded_class_attribute
                ),
                **self.forwarded_attributes,
            )(
                *forwarded_children,
                Div(_class="absolute right-4 top-4")(
                    DialogClose()(XIcon(), Span(_class="sr-only")("Close"))
                ),
            )
        )

        return self


class DialogHeader(Div):
    def __init__(self, **attributes: Unpack[DivAttributes]):
        base_class_attribute = "flex-col text-center gap-2 flex sm:text-left"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            **attributes,
        )


class DialogBody(Section):
    def __init__(self, **attributes: Unpack[SectionAttributes]):
        base_class_attribute = "flex-1 px-6 -mx-6"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            **attributes,
        )


class DialogFooter(Div):
    def __init__(self, **attributes: Unpack[DivAttributes]):
        base_class_attribute = "flex-col-reverse gap-2 flex sm:justify-end sm:flex-row"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            **attributes,
        )

    def __call__(self, *children: tuple) -> Self:
        for child in children:
            if (
                isinstance(child, str)
                or isinstance(child, BaseWebElement)
                or not isinstance(child, Iterable)
            ):
                if isinstance(child, BaseWebElement):
                    # If a child has a `@click.close` attribute, close the dialog when it's clicked
                    should_close = child.attributes.pop("@click.close", False)
                    if should_close:
                        child.attributes["@click"] = (
                            "$dispatch('reset-form-data'); modalIsOpen = false; $refs.dialog.close()"
                        )
                self.children.append(child)
            elif isinstance(child, Generator):
                self.children.extend(list(child))
            elif isinstance(child, type(None)):
                continue
            else:
                self.children.extend(child)

        return self


class DialogTitle(H2):
    def __init__(self, **attributes: Unpack[HAttributes]):
        base_class_attribute = "leading-none font-semibold text-lg"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            **attributes,
        )


class DialogDescription(P):
    def __init__(self, **attributes: Unpack[PAttributes]):
        base_class_attribute = "text-muted-foreground text-sm"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            **attributes,
        )
