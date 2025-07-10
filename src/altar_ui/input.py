import warnings
from typing import Self

from aether.plugins.alpinejs import AlpineJSData, alpine_js_data_merge
from aether.plugins.tailwindcss import tw_merge
from aether.tags.html import (
    Div,
    DivAttributes,
)
from aether.tags.html import (
    Input as PyInput,
)
from aether.tags.html import (
    InputAttributes as PyInputAttributes,
)
from altar_icons import EyeIcon, EyeOffIcon

from .button import Button

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack  # noqa: UP035


class Input(PyInput):
    def __init__(self, **attributes: Unpack[PyInputAttributes]):
        base_class_attribute = (
            "flex h-9 w-full min-w-0 rounded-md border bg-transparent px-3 py-1 text-base shadow-xs transition-[color,box-shadow] dark:bg-input/30  border-input outline-none "
            "focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px] "
            "placeholder:text-muted-foreground "
            "selection:bg-primary selection:text-primary-foreground md:text-sm "
            "file:text-foreground file:inline-flex file:h-7 file:border-0 file:bg-transparent file:text-sm file:font-medium "
            "disabled:pointer-events-none disabled:cursor-not-allowed disabled:opacity-50 "
            "aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 aria-invalid:border-destructive"
        )
        class_attribute = attributes.pop("_class", "")
        data_slot = attributes.pop("data_slot", "input")

        super().__init__(
            _class=tw_merge(class_attribute, base_class_attribute),
            data_slot=data_slot,
            **attributes,
        )


class PasswordInput(Div):
    def __init__(self, **attributes: Unpack[DivAttributes]):
        base_class_attribute = "flex relative items-center rounded-md"
        base_x_data_attribute = AlpineJSData(
            data={"showPassword": False}, directive="x-data"
        )
        x_data_attribute = attributes.pop("x_data", None)

        self.forwarded_class_attribute = attributes.pop("_class", "")
        self.forwarded_attributes = attributes

        super().__init__(
            _class=base_class_attribute,
            x_data=alpine_js_data_merge(base_x_data_attribute, x_data_attribute),
        )

        self.children.extend(
            [
                Input(
                    type="password",
                    _class=self.forwarded_class_attribute,
                    **{":type": "showPassword? 'text' : 'password'"},
                    **self.forwarded_attributes,
                ),
                Button(
                    type="button",
                    size="icon",
                    variant="ghost",
                    _class="absolute top-1/2 right-1 w-6 h-6 text-muted-foreground rounded-md -translate-y-1/2",
                    **{"@click": "showPassword = !showPassword"},
                )(
                    EyeOffIcon(x_show="!showPassword", _class="w-4 h-4"),
                    EyeIcon(x_show="showPassword", _class="w-4 h-4"),
                ),
            ]
        )

    def __call__(self, *_children: tuple) -> Self:
        warnings.warn(
            f"Trying to add child to a non-child element: {self.__class__.__qualname__}",
            UserWarning,
            stacklevel=2,
        )

        return self
