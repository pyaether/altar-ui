from enum import Enum
from typing import Literal

from pytempl.plugins.tailwindcss import tw_merge
from pytempl.tags.html import Label as PyLabel
from pytempl.tags.html import LabelAttributes as PyLabelAttributes

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class LabelVariant(Enum):
    default = "text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"


class Label(PyLabel):
    def __init__(
        self,
        _for: str = "",
        variant: Literal["default"] = "default",
        **attributes: Unpack[PyLabelAttributes],
    ):
        base_class_attribute = ""
        class_attribute = attributes.pop("_class", "")
        variant_class_attribute = LabelVariant[variant]

        if _for:
            attributes["_for"] = _for

        super().__init__(
            _class=tw_merge(
                class_attribute,
                f"{variant_class_attribute.value} {base_class_attribute}",
            ),
            **attributes,
        )
