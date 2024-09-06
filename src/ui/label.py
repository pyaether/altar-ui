from enum import Enum
from typing import Any, Dict, Literal

from pytempl import html_class_merge
from pytempl.tags import Label as PyLabel


class LabelVariant(Enum):
    default = "text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"


class Label(PyLabel):
    def __init__(
        self,
        _for: str = "",
        variant: Literal["default"] = "default",
        **attributes: Dict[str, Any],
    ):
        base_class_attribute = ""
        class_attribute = attributes.pop("_class", "")
        variant_class_attribute = LabelVariant[variant]

        if _for:
            attributes["_for"] = _for

        super().__init__(
            _class=html_class_merge(
                class_attribute,
                f"{variant_class_attribute.value} {base_class_attribute}",
            ),
            **attributes,
        )
