import warnings
from typing import Self

from aether.plugins.alpinejs import AlpineJSData, Statement, alpine_js_data_merge
from aether.plugins.tailwindcss import tw_merge
from aether.tags.html import (
    Textarea as PyTextarea,
)
from aether.tags.html import (
    TextareaAttributes as PyTextareaAttributes,
)

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class Textarea(PyTextarea):
    def __init__(
        self, autogrow: bool = False, **attributes: Unpack[PyTextareaAttributes]
    ):
        base_class_attribute = "border-input placeholder:text-muted-foreground focus-visible:border-ring focus-visible:ring-ring/50 aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 aria-invalid:border-destructive dark:bg-input/30 flex field-sizing-content min-h-16 w-full rounded-md border bg-transparent px-3 py-2 text-base shadow-xs transition-[color,box-shadow] outline-none focus-visible:ring-[3px] disabled:cursor-not-allowed disabled:opacity-50 md:text-sm"
        class_attribute = attributes.pop("_class", "")

        if autogrow:
            base_x_data_attribute = AlpineJSData(
                data={
                    "resize()": Statement(
                        "{ $el.style.height = '0px'; $el.style.height = $el.scrollHeight + 'px'; }",
                        seq_type="definition",
                    )
                },
                directive="x-data",
            )
            x_data_attribute = attributes.pop("x_data", None)

            attributes["x-data"] = alpine_js_data_merge(
                base_x_data_attribute, x_data_attribute
            )
            attributes["x-effect"] = "resize()"
            attributes["@input"] = "resize()"

        super().__init__(
            _class=tw_merge(class_attribute, base_class_attribute),
            data_slot="textarea",
            **attributes,
        )

    def __call__(self, *_children: tuple) -> Self:
        warnings.warn(
            f"Trying to add child to a non-child element: {self.__class__.__qualname__}",
            UserWarning,
            stacklevel=2,
        )

        return self
