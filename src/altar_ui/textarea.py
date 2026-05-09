"""Textarea

Displays a form textarea or a component that looks like a textarea.

Composition:
    Use the following composition to build a Textarea:

    Textarea
"""

import warnings
from typing import Self

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
    from typing_extensions import Unpack  # noqa: UP035


class Textarea(PyTextarea):
    def __init__(self, **attributes: Unpack[PyTextareaAttributes]):
        base_class_attribute = "field-sizing-content outline-none transition-[color,box-shadow] rounded-md border-input shadow-xs border min-h-16 text-base flex px-3 bg-transparent py-2 w-full md:text-sm dark:bg-input/30 aria-invalid:border-destructive aria-invalid:ring-destructive/20 focus-visible:border-ring focus-visible:ring-[3px] focus-visible:ring-ring/50 disabled:opacity-50 disabled:cursor-not-allowed placeholder:text-muted-foreground dark:aria-invalid:ring-destructive/40"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute), **attributes
        )

    def __call__(self, *_children: tuple) -> Self:
        warnings.warn(
            f"Trying to add child to a non-child element: {self.__class__.__qualname__}",
            UserWarning,
            stacklevel=2,
        )

        return self
