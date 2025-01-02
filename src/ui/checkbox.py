from pytempl.plugins.tailwindcss import tw_merge
from pytempl.tags.html import Div, DivAttributes, Input
from pytempl_icons import CheckIcon

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class Checkbox(Div):
    def __init__(
        self,
        id: str,
        value: str,
        **attributes: Unpack[DivAttributes],
    ):
        class_attribute = "relative flex items-center"

        forwarded_base_class_attribute = "peer cursor-pointer appearance-none h-4 w-4 shrink-0 rounded-sm border border-primary shadow focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50 checked:bg-primary"
        forwarded_class_attribute = attributes.pop("_class", "")
        forwarded_attributes = attributes

        super().__init__(
            id=id,
            _class=class_attribute,
        )

        self.children = [
            Input(
                type="checkbox",
                x_model=id,
                value=value,
                _class=tw_merge(
                    forwarded_class_attribute, forwarded_base_class_attribute
                ),
                **forwarded_attributes,
            ),
            CheckIcon(
                _class="pointer-events-none invisible absolute inset-0 peer-checked:text-primary-foreground peer-checked:visible h-4 w-4",
            ),
        ]
