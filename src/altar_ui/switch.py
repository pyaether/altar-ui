"""Switch

A control that allows the user to toggle between checked and not checked.

Composition:
    Use the following composition to build a Switch:

    Switch
"""

from aether.plugins.tailwindcss import tw_merge
from aether.tags.html import Input as PyInput
from aether.tags.html import InputAttributes

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack  # noqa: UP035


class Switch(PyInput):
    def __init__(self, **attributes: Unpack[InputAttributes]):
        base_class_attribute = "outline-none appearance-none inline-flex transition-all rounded-full border-transparent shadow-xs border shrink-0 items-center bg-input w-8 h-[1.15rem] dark:bg-input/80 checked:bg-primary focus-visible:border-ring focus-visible:ring-[3px] focus-visible:ring-ring/50 disabled:opacity-50 disabled:cursor-not-allowed before:pointer-events-none before:transition-all before:rounded-full before:content-[''] before:block before:size-4 before:ring-0 before:bg-background dark:checked:bg-primary dark:before:bg-foreground checked:before:ms-3.5 dark:checked:before:bg-primary-foreground"
        class_attribute = attributes.pop("_class", "")

        type_attribute = attributes.pop("type", "checkbox")
        role_attribute = attributes.pop("role", "switch")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            type=type_attribute,
            role=role_attribute,
            **attributes,
        )
