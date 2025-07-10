from aether.plugins.tailwindcss import tw_merge
from aether.tags.html import Label as PyLabel
from aether.tags.html import LabelAttributes as PyLabelAttributes

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack  # noqa: UP035


class Label(PyLabel):
    def __init__(
        self,
        **attributes: Unpack[PyLabelAttributes],
    ):
        base_class_attribute = "flex gap-2 items-center font-medium text-sm select-none leading-none group-data-[disabled=true]:pointer-events-none group-data-[disabled=true]:opacity-50 peer-disabled:cursor-not-allowed peer-disabled:opacity-50"
        class_attribute = attributes.pop("_class", "")
        data_slot = attributes.pop("data_slot", "label")

        super().__init__(
            _class=tw_merge(class_attribute, base_class_attribute),
            data_slot=data_slot,
            **attributes,
        )
