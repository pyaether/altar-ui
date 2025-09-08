from collections.abc import Generator, Iterable
from typing import Literal, Self

from aether import BaseWebElement
from aether.plugins.alpinejs import AlpineJSData, alpine_js_data_merge
from aether.plugins.tailwindcss import tw_merge
from aether.tags.html import H2, Div, DivAttributes, HAttributes, P, PAttributes, Span
from aether.tags.html import Button as PyButton
from aether.tags.html import ButtonAttributes as PyButtonAttributes
from altar_icons import CrossIcon

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
            data_slot="dialog",
            **attributes,
        )


class DialogTrigger(Button):
    def __init__(
        self,
        variant: Literal[
            "default", "destructive", "outline", "secondary", "ghost", "link"
        ] = "default",
        size: Literal["default", "sm", "lg", "icon"] = "default",
        **attributes: Unpack[PyButtonAttributes],
    ):
        super().__init__(
            type="button",
            variant=variant,
            size=size,
            data_slot="dialog-trigger",
            **{"@click": "modalIsOpen = true"},
            **attributes,
        )


class DialogClose(PyButton):
    def __init__(self, **attributes: Unpack[PyButtonAttributes]):
        super().__init__(
            type="button",
            data_slot="dialog-close",
            **{
                "@click": "$dispatch('reset-form-data'); modalIsOpen = false",
                ":class": "{ 'bg-accent': modalIsOpen, 'text-muted-foreground': modalIsOpen }",
            },
            **attributes,
        )


class DialogOverlay(Div):
    def __init__(self, **attributes: Unpack[DivAttributes]):
        base_class_attribute = "fixed inset-0 z-50 bg-black/50 backdrop-blur-md"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            x_show="modalIsOpen",
            x_cloak=True,
            data_slot="dialog-overlay",
            _class=tw_merge(base_class_attribute, class_attribute),
            **{"x-transition.opacity.duration.100ms": True},
            **attributes,
        )


class DialogContent(Div):
    def __init__(self, **attributes: Unpack[DivAttributes]):
        self.forwarded_base_class_attribute = "grid fixed top-[50%] left-[50%] z-50 gap-4 p-6 w-full max-w-[calc(100%-2rem)] bg-background rounded-lg border shadow-lg duration-200 translate-x-[-50%] translate-y-[-50%] sm:max-w-lg"
        self.forwarded_class_attribute = attributes.pop("_class", "")
        self.forwarded_attributes = attributes

        super().__init__(
            x_show="modalIsOpen",
            data_slot="dialog-portal",
            **{
                "x-trap.noscroll": "modalIsOpen",
                "@keydown.esc.window": "modalIsOpen = false",
                "@click.self": "modalIsOpen = false",
                ":aria_labelledby": "$id('dialog-portal')",
            },
            aria_modal="true",
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

        self.children.extend(
            [
                DialogOverlay()(),
                Div(
                    data_slot="dialog-content",
                    _class=tw_merge(
                        self.forwarded_base_class_attribute,
                        self.forwarded_class_attribute,
                    ),
                    **{
                        "x-transition:enter": "animate-in zoom-in-95 fade-in-0",
                        "x-transition:leave": "animate-out zoom-out-95 fade-out-0",
                    },
                    **self.forwarded_attributes,
                )(
                    *forwarded_children,
                    DialogClose(
                        _class="absolute top-4 right-4 rounded-xs ring-offset-background opacity-70 transition-opacity [&_svg:not([class*='size-'])]:size-4 disabled:pointer-events-none hover:opacity-100 focus:outline-hidden focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 [&_svg]:pointer-events-none [&_svg]:shrink-0"
                    )(CrossIcon(), Span(_class="sr-only")("Close")),
                ),
            ]
        )

        return self


class DialogHeader(Div):
    def __init__(self, **attributes: Unpack[DivAttributes]):
        base_class_attribute = "flex flex-col gap-2 text-center sm:text-left"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            data_slot="dialog-header",
            _class=tw_merge(base_class_attribute, class_attribute),
            **attributes,
        )


class DialogFooter(Div):
    def __init__(self, **attributes: Unpack[DivAttributes]):
        base_class_attribute = "flex flex-col-reverse gap-2 sm:flex-row sm:justify-end"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            data_slot="dialog-footer",
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
                            "$dispatch('reset-form-data'); modalIsOpen = false"
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
        base_class_attribute = "font-semibold text-lg leading-none"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            data_slot="dialog-title",
            _class=tw_merge(base_class_attribute, class_attribute),
            **attributes,
        )


class DialogDescription(P):
    def __init__(self, **attributes: Unpack[PAttributes]):
        base_class_attribute = "text-muted-foreground text-sm"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            data_slot="dialog-description",
            _class=tw_merge(base_class_attribute, class_attribute),
            **attributes,
        )
