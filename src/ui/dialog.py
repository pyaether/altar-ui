from typing import Any, Dict, Generator, Iterable, Literal, Self, Tuple

from pytempl import BaseWebElement, html_class_merge
from pytempl.tags import H3, Div, Span
from pytempl.tags import Button as PyButton
from pytempl_icons import CrossIcon

from .button import Button


class Dialog(Div):
    def __init__(self, **attributes: Dict[str, Any]):
        super().__init__(x_data="{ modalIsOpen: false }", **attributes)


class DialogTrigger(Button):
    def __init__(
        self,
        variant: Literal[
            "default", "destructive", "outline", "secondary", "ghost", "link"
        ] = "default",
        size: Literal["default", "sm", "lg", "icon"] = "default",
        **attributes: Dict[str, Any],
    ):
        super().__init__(
            type="button",
            variant=variant,
            size=size,
            **{"@click": "modalIsOpen = true"},
            **attributes,
        )


class DialogClose(PyButton):
    def __init__(self):
        super().__init__(
            **{"@click": "modalIsOpen = false"},
            aria_label="close modal",
            _class="absolute right-4 top-4 rounded-sm opacity-70 ring-offset-background transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:pointer-events-none",
            **{
                ":class": "modalIsOpen ? 'bg-accent text-muted-foreground' : ''",
            },
        )


class DialogOverlay(Div):
    def __init__(self, **attributes: Dict[str, Any]):
        base_class_attribute = "fixed inset-0 z-50 backdrop-blur-md bg-black/50"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            x_show="modalIsOpen",
            _class=html_class_merge(class_attribute, base_class_attribute),
            **{
                "x-transition.opacity.duration.100ms": True,
                ":class": "modalIsOpen ? 'animate-in fade-in-0' : 'animate-out fade-out-0'",
            },
            **attributes,
        )


class DialogContent(Div):
    def __init__(self, **attributes: Dict[str, Any]):
        self.forwarded_base_class_attribute = "fixed left-[50%] top-[50%] z-50 grid w-full max-w-lg translate-x-[-50%] translate-y-[-50%] gap-4 border bg-background p-6 shadow-lg duration-200 sm:rounded-lg"
        self.forwarded_class_attribute = attributes.pop("_class", "")
        self.forwarded_attributes = attributes

        super().__init__(
            x_show="modalIsOpen",
            x_cloak=True,
            **{
                "x-trap.inert.noscroll": "modalIsOpen",
                "@keydown.esc.window": "modalIsOpen = false",
                "@click.self": "modalIsOpen = false",
            },
            aria_modal="true",
            aria_labelledby="$id('dialog-title')",
        )

    def __call__(self, *children: Tuple) -> Self:
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
                    _class=html_class_merge(
                        self.forwarded_class_attribute,
                        self.forwarded_base_class_attribute,
                    ),
                    **self.forwarded_attributes,
                )(
                    *forwarded_children,
                    DialogClose()(
                        CrossIcon(_class="h-4 w-4"), Span(_class="sr-only")("Close")
                    ),
                ),
            ]
        )

        return self


class DialogHeader(H3):
    def __init__(self, **attributes: Dict[str, Any]):
        base_class_attribute = "flex flex-col space-y-1.5 text-center sm:text-left"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=html_class_merge(class_attribute, base_class_attribute), **attributes
        )


class DialogFooter(Div):
    def __init__(self, **attributes: Dict[str, Any]):
        base_class_attribute = (
            "flex flex-col-reverse sm:flex-row sm:justify-end sm:space-x-2"
        )
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=html_class_merge(class_attribute, base_class_attribute), **attributes
        )

    def __call__(self, *children: Tuple) -> Self:
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
                        child.attributes["@click"] = "modalIsOpen = false"
                self.children.append(child)
            elif isinstance(child, Generator):
                self.children.extend(list(child))
            elif isinstance(child, type(None)):
                continue
            else:
                self.children.extend(child)

        return self


class DialogTitle(H3):
    def __init__(self, **attributes: Dict[str, Any]):
        base_class_attribute = "text-lg font-semibold leading-none tracking-tight"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=html_class_merge(class_attribute, base_class_attribute), **attributes
        )


class DialogBody(Div):
    def __init__(self, **attributes: Dict[str, Any]):
        base_class_attribute = "text-sm text-muted-foreground"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=html_class_merge(class_attribute, base_class_attribute), **attributes
        )
