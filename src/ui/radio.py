from typing import Any, Dict

from pytempl.plugins.tailwindcss import tw_merge
from pytempl.tags.html import Div, Input
from pytempl_icons import DotFilledIcon


class RadioGroup(Div):
    def __init__(self, default_value: str, **attributes: Dict[str, Any]):
        base_class_attribute = "grid gap-2"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(class_attribute, base_class_attribute),
            x_data=f"{{ selectedRadioItem: '{default_value}' }}",
            **attributes,
        )


class RadioGroupItem(Div):
    def __init__(
        self,
        id: str,
        value: str,
        name: str = "",
        **attributes: Dict[str, Any],
    ):
        class_attribute = "relative flex items-center justify-start"

        forwarded_base_class_attribute = "peer cursor-pointer appearance-none h-4 w-4 shrink-0 rounded-full border border-primary shadow focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50 checked:bg-primary"
        forwarded_class_attribute = attributes.pop("_class", "")
        forwarded_attributes = attributes

        super().__init__(_class=f"{class_attribute}")

        self.children = [
            Input(
                type="radio",
                id=id,
                value=value,
                name=name if name else "radio_group",
                x_model="selectedRadioItem",
                _class=tw_merge(
                    forwarded_class_attribute, forwarded_base_class_attribute
                ),
                **forwarded_attributes,
            ),
            DotFilledIcon(
                _class="pointer-events-none invisible absolute inset-0 peer-checked:text-primary-foreground peer-checked:visible h-4 w-4",
            ),
        ]
