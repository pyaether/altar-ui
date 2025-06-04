import warnings
from typing import Literal, Self

from aether.plugins.tailwindcss import tw_merge
from aether.tags.html import Div, DivAttributes

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class Separator(Div):
    def __init__(
        self,
        orientation: Literal["horizontal", "vertical"] = "horizontal",
        decorative: bool = True,
        **attributes: Unpack[DivAttributes],
    ):
        base_class_attribute = "bg-border shrink-0"
        data_orientation_class_attribute = "data-[orientation=horizontal]:h-px data-[orientation=horizontal]:w-full data-[orientation=vertical]:h-full data-[orientation=vertical]:w-px"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(
                class_attribute,
                f"{base_class_attribute} {data_orientation_class_attribute}",
            ),
            data_slot="separator-root",
            data_orientation=orientation,
            role="separator" if decorative else "none",
            aria_orientation=orientation,
            **attributes,
        )

    def __call__(self, *_children: tuple) -> Self:
        warnings.warn(
            f"Trying to add child to a non-child element: {self.__class__.__qualname__}",
            UserWarning,
            stacklevel=2,
        )

        return self
