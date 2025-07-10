import warnings
from typing import Self

from aether.plugins.tailwindcss import tw_merge
from aether.tags.html import Div, Input, InputAttributes
from altar_icons import CheckIcon

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack  # noqa: UP035


class Checkbox(Div):
    def __init__(self, **attributes: Unpack[InputAttributes]):
        class_attribute = "peer relative inline-flex items-center"

        if attributes.get("id"):
            forwarded_id_attribute = attributes.pop("id")
        elif attributes.get(":id"):
            forwarded_id_attribute = attributes.pop(":id")
        else:
            forwarded_id_attribute = "$id('checkbox')"

        forwarded_base_class_attribute = "rounded-[4px] border-input border outline-none shadow-xs transition-shadow appearance-none cursor-pointer peer aria-invalid:ring-destructive/20 aria-invalid:border-destructive size-4 shrink-0 dark:bg-input/30 dark:aria-invalid:ring-destructive/40 checked:text-primary-foreground checked:bg-primary checked:border-primary disabled:opacity-50 disabled:cursor-not-allowed focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px] dark:checked:bg-primary"
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
                _class="absolute inset-0 invisible pointer-events-none peer-checked:text-primary-foreground peer-checked:transition-none peer-checked:visible size-4",
            ),
        ]

    def __call__(self, *_children: tuple) -> Self:
        warnings.warn(
            f"Trying to add child to a non-child element: {self.__class__.__qualname__}",
            UserWarning,
            stacklevel=2,
        )

        return self
