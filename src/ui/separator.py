from typing import Literal

from pytempl.plugins.tailwindcss import tw_merge
from pytempl.tags.html import Div, DivAttributes

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class Separator(Div):
    have_children = False

    def __init__(
        self,
        orientation: Literal["horizontal", "vertical"] = "horizontal",
        decorative: bool = True,
        **attributes: Unpack[DivAttributes],
    ):
        base_class_attribute = "shrink-0 bg-border"
        class_attribute = attributes.pop("_class", "")
        orientation_class_attribute = (
            "h-[1px] w-full" if orientation == "horizontal" else "h-full w-[1px]"
        )

        super().__init__(
            _class=tw_merge(
                class_attribute, f"{base_class_attribute} {orientation_class_attribute}"
            ),
            role="separator" if decorative else "none",
            aria_orientation=orientation,
            **attributes,
        )
