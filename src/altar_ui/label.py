"""Label

Renders an accessible label associated with controls.

Composition:
    Use the following composition to build a Label:

    Label
"""

from aether.plugins.tailwindcss import tw_merge
from aether.tags.html import Label as PyLabel
from aether.tags.html import LabelAttributes as PyLabelAttributes

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack  # noqa: UP035


class Label(PyLabel):
    def __init__(self, **attributes: Unpack[PyLabelAttributes]):
        base_class_attribute = "leading-none select-none items-center font-medium text-sm gap-2 flex peer-disabled:pointer-events-none peer-disabled:opacity-50 has-[>*:disabled]:pointer-events-none has-[+*:disabled]:pointer-events-none has-[>*:disabled]:opacity-50 has-[+*:disabled]:opacity-50"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            **attributes,
        )
