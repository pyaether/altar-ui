from pytempl.plugins.tailwindcss import tw_merge
from pytempl.tags.html import (
    Div,
    DivAttributes,
)
from pytempl.tags.html import (
    Input as PyInput,
)
from pytempl.tags.html import (
    InputAttributes as PyInputAttributes,
)
from pytempl_icons import EyeIcon, EyeOffIcon

from .button import Button

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class Input(PyInput):
    def __init__(self, **attributes: Unpack[PyInputAttributes]):
        base_class_attribute = "flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            type=type,
            _class=tw_merge(class_attribute, base_class_attribute),
            **attributes,
        )


class PasswordInput(Div):
    def __init__(self, **attributes: Unpack[DivAttributes]):
        base_class_attribute = "flex items-center relative rounded-md"
        forwarded_class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=base_class_attribute,
            x_data="{ showPassword: false }",
        )

        self.children.extend(
            [
                Input(
                    type="password",
                    _class=forwarded_class_attribute,
                    **{":type": "showPassword? 'text' : 'password'"},
                    **attributes,
                ),
                Button(
                    type="button",
                    size="icon",
                    variant="ghost",
                    _class="absolute right-1 top-1/2 h-6 w-6 -translate-y-1/2 rounded-md text-muted-foreground",
                    **{"@click": "showPassword = !showPassword"},
                )(
                    EyeOffIcon(x_show="!showPassword", _class="h-4 w-4"),
                    EyeIcon(x_show="showPassword", _class="h-4 w-4"),
                ),
            ]
        )
