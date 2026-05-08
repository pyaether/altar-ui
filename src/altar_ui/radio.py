"""Radio

Input button where no more than one of the buttons can be checked at a time.

Composition:
    Use the following composition to build a Radio:

    Radio
"""

from aether.plugins.tailwindcss import tw_merge
from aether.tags.html import Input as PyInput
from aether.tags.html import InputAttributes

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack  # noqa: UP035


class Radio(PyInput):
    def __init__(
        self,
        name: str,
        value: str,
        checked: bool = False,
        **attributes: Unpack[InputAttributes],
    ):
        base_class_attribute = "outline-none appearance-none transition-[color,box-shadow] relative rounded-full border-input shadow-xs border shrink-0 text-primary size-4 aspect-square dark:bg-input/30 aria-invalid:border-destructive aria-invalid:ring-destructive/20 focus-visible:border-ring focus-visible:ring-[3px] focus-visible:ring-ring/50 disabled:opacity-50 disabled:cursor-not-allowed dark:aria-invalid:ring-destructive/40 checked:before:absolute checked:before:rounded-full checked:before:content-[''] checked:before:left-1/2 checked:before:size-2 checked:before:top-1/2 checked:before:bg-primary checked:before:-translate-x-1/2 checked:before:-translate-y-1/2"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            name=name,
            value=value,
            checked=checked,
            type="radio",
            role="radio",
            **attributes,
        )
