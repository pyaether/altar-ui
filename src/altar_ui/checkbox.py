import warnings
from typing import Self

from aether.plugins.tailwindcss import tw_merge
from aether.tags.html import Div, Input, InputAttributes
from altar_icons import CheckIcon

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class Checkbox(Div):
    def __init__(self, **attributes: Unpack[InputAttributes]):
        class_attribute = "peer relative inline-flex items-center"

        if attributes.get("id"):
            forwarded_id_attribute = attributes.pop("id")
        elif attributes.get(":id"):
            forwarded_id_attribute = attributes.pop(":id")
        else:
            forwarded_id_attribute = "$id('checkbox')"

        forwarded_base_class_attribute = "peer cursor-pointer appearance-none border-input dark:bg-input/30 checked:bg-primary checked:text-primary-foreground dark:checked:bg-primary checked:border-primary focus-visible:border-ring focus-visible:ring-ring/50 aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 aria-invalid:border-destructive size-4 shrink-0 rounded-[4px] border shadow-xs transition-shadow outline-none focus-visible:ring-[3px] disabled:cursor-not-allowed disabled:opacity-50"
        self.forwarded_class_attribute = attributes.pop("_class", "")
        self.forwarded_attributes = attributes

        super().__init__(
            _class=class_attribute,
        )

        self.children = [
            Input(
                type="checkbox",
                data_slot="checkbox",
                _class=tw_merge(
                    self.forwarded_class_attribute, forwarded_base_class_attribute
                ),
                **{":id": forwarded_id_attribute}
                if "$id" in forwarded_id_attribute
                else {"id": f"{forwarded_id_attribute.lower().replace(' ', '-')}"},
                **self.forwarded_attributes,
            ),
            CheckIcon(
                data_slot="checkbox-indicator",
                _class="pointer-events-none invisible absolute inset-0 peer-checked:text-primary-foreground peer-checked:transition-none peer-checked:visible size-4",
            ),
        ]

    def __call__(self, *_children: tuple) -> Self:
        warnings.warn(
            f"Trying to add child to a non-child element: {self.__class__.__qualname__}",
            UserWarning,
            stacklevel=2,
        )

        return self
