import warnings
from typing import Self

from aether.plugins.alpinejs import AlpineJSData, alpine_js_data_merge
from aether.plugins.tailwindcss import tw_merge
from aether.tags.html import Div, DivAttributes, Input
from altar_icons import CircleIcon

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class RadioGroup(Div):
    def __init__(
        self,
        default_value: str,
        **attributes: Unpack[DivAttributes],
    ):
        base_class_attribute = "grid gap-3"
        base_x_data_attribute = AlpineJSData(
            data={"selectedRadioItem": default_value}, directive="x-data"
        )
        class_attribute = attributes.pop("_class", "")
        x_data_attribute = attributes.pop("x_data", None)

        super().__init__(
            _class=tw_merge(class_attribute, base_class_attribute),
            data_slot="radio-group",
            x_model="selectedRadioItem" if attributes.get("x_modelable") else None,
            x_data=alpine_js_data_merge(base_x_data_attribute, x_data_attribute),
            **attributes,
        )


class RadioGroupItem(Div):
    def __init__(self, **attributes: Unpack[DivAttributes]):
        class_attribute = "peer relative inline-flex items-center justify-center"

        if attributes.get("id"):
            forwarded_id_attribute = attributes.pop("id")
        elif attributes.get(":id"):
            forwarded_id_attribute = attributes.pop(":id")
        else:
            forwarded_id_attribute = "$id('radio-group-item')"

        forwarded_base_class_attribute = "text-primary rounded-full border-input border outline-none shadow-xs transition-[color,box-shadow] appearance-none cursor-pointer peer aria-invalid:ring-destructive/20 aria-invalid:border-destructive aspect-square size-4 shrink-0 dark:bg-input/30 dark:aria-invalid:ring-destructive/40 disabled:opacity-50 disabled:cursor-not-allowed focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px]"
        self.forwarded_class_attribute = attributes.pop("_class", "")
        forwarded_name_attribute = attributes.pop("name", "radio-group")
        self.forwarded_attributes = attributes

        super().__init__(_class=f"{class_attribute}")

        self.children = [
            Input(
                type="radio",
                data_slot="radio-group-item",
                name=forwarded_name_attribute,
                _class=tw_merge(
                    self.forwarded_class_attribute, forwarded_base_class_attribute
                ),
                x_model="selectedRadioItem",
                **{":id": forwarded_id_attribute}
                if "$id" in forwarded_id_attribute
                else {"id": f"{forwarded_id_attribute.lower().replace(' ', '-')}"},
                **self.forwarded_attributes,
            ),
            CircleIcon(
                data_slot="radio-group-indicator",
                _class="absolute top-1/2 left-1/2 invisible pointer-events-none fill-primary size-2 -translate-x-1/2 -translate-y-1/2 peer-checked:visible",
            ),
        ]

    def __call__(self, *_children: tuple) -> Self:
        warnings.warn(
            f"Trying to add child to a non-child element: {self.__class__.__qualname__}",
            UserWarning,
            stacklevel=2,
        )
        return self
