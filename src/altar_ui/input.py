"""Input

Displays a form input field or a component that looks like an input field.

Composition:
    Use the following composition to build an Input:

    Input
"""

from aether.plugins.tailwindcss import tw_merge
from aether.tags.html import (
    Input as PyInput,
)
from aether.tags.html import (
    InputAttributes as PyInputAttributes,
)

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack  # noqa: UP035


class Input(PyInput):
    def __init__(self, **attributes: Unpack[PyInputAttributes]):
        base_class_attribute = "outline-none appearance-none transition-[color,box-shadow] rounded-md border-input shadow-xs border min-w-0 text-base flex px-3 bg-transparent py-1 w-full h-9 md:text-sm dark:bg-input/30 aria-invalid:border-destructive aria-invalid:ring-destructive/20 focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px] disabled:pointer-events-none disabled:opacity-50 disabled:cursor-not-allowed selection:text-primary-foreground selection:bg-primary file:inline-flex file:border-0 file:font-medium file:text-foreground file:text-sm file:bg-transparent file:h-7 placeholder:text-muted-foreground dark:aria-invalid:ring-destructive/40"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute), **attributes
        )
