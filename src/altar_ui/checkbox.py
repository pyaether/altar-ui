"""Checkbox

A control that allows the user to toggle between checked and not checked.

Composition:
    Use the following composition to build a Checkbox:

    Checkbox
"""

import warnings
from typing import Self

from aether.plugins.tailwindcss import tw_merge
from aether.tags.html import Div, Input, InputAttributes
from altar_icons import CheckIcon

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack  # noqa: UP035


class Checkbox(Div):
    def __init__(self, **attributes: Unpack[InputAttributes]):
        base_class_attribute = (
            "relative inline-flex shrink-0 size-4 items-center justify-center"
        )

        if not attributes.get("id") and not attributes.get(":id"):
            attributes[":id"] = "$id('checkbox')"

        forwarded_base_class_attribute = "outline-none appearance-none transition-shadow rounded-[4px] border-input shadow-xs border size-4 m-0 peer dark:bg-input/30 aria-invalid:border-destructive aria-invalid:ring-destructive/20 checked:border-primary checked:bg-primary focus-visible:border-ring focus-visible:ring-[3px] focus-visible:ring-ring/50 disabled:opacity-50 disabled:cursor-not-allowed dark:aria-invalid:ring-destructive/40 dark:checked:bg-primary"
        forwarded_class_attribute = attributes.pop("_class", "")
        self.forwarded_attributes = attributes

        super().__init__(_class=base_class_attribute)

        self.children = [
            Input(
                type="checkbox",
                _class=tw_merge(
                    forwarded_base_class_attribute, forwarded_class_attribute
                ),
                **self.forwarded_attributes,
            ),
            CheckIcon(
                _class="pointer-events-none absolute opacity-0 text-primary-foreground size-3.5 peer-checked:opacity-100 peer-disabled:opacity-50",
                aria_hidden="true",
            ),
        ]

    def __call__(self, *_children: tuple) -> Self:
        warnings.warn(
            f"Trying to add child to a non-child element: {self.__class__.__qualname__}",
            UserWarning,
            stacklevel=2,
        )

        return self
