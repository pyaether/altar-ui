import warnings
from typing import Self

from aether.plugins.alpinejs import AlpineJSData, alpine_js_data_merge
from aether.plugins.tailwindcss import tw_merge
from aether.tags.html import Button, Div, DivAttributes, Input, Span

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class Switch(Div):
    def __init__(
        self,
        default_value: bool = False,
        disabled: bool = False,
        **attributes: Unpack[DivAttributes],
    ):
        base_class_attribute = "inline-flex relative items-center peer"
        base_x_data_attribute = AlpineJSData(
            data={"checked": default_value}, directive="x-data"
        )
        x_data_attribute = attributes.pop("x_data", None)

        if attributes.get("id"):
            forwarded_id_attribute = attributes.pop("id")
        elif attributes.get(":id"):
            forwarded_id_attribute = attributes.pop(":id")
        else:
            forwarded_id_attribute = "$id('switch')"

        forwarded_base_class_attribute = "inline-flex items-center w-8 h-[1.15rem] rounded-full border border-transparent outline-none shadow-xs transition-all appearance-none cursor-pointer peer shrink-0 disabled:opacity-50 disabled:cursor-not-allowed focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px]"
        self.forwarded_class_attribute = attributes.pop("_class", "")
        forwarded_name_attribute = attributes.pop("name", "toggle-switch")
        self.forwarded_attributes = attributes

        super().__init__(
            _class=base_class_attribute,
            x_data=alpine_js_data_merge(base_x_data_attribute, x_data_attribute),
        )

        self.children = [
            Input(
                type="hidden",
                name=forwarded_name_attribute,
                x_model="checked",
                disabled=disabled,
            ),
            Button(
                type="button",
                data_slot="switch-thumb",
                disabled=disabled,
                x_model="checked" if attributes.get("x_modelable") else None,
                _class=tw_merge(
                    self.forwarded_class_attribute, forwarded_base_class_attribute
                ),
                **{":id": forwarded_id_attribute}
                if "$id" in forwarded_id_attribute
                else {"id": f"{forwarded_id_attribute.lower().replace(' ', '-')}"},
                **{
                    "@click": "checked = !checked",
                    ":class": "{ 'bg-primary': checked, 'bg-input dark:bg-input/80': !checked }",
                },
                **self.forwarded_attributes,
            )(
                Span(
                    _class="block bg-background rounded-full ring-0 transition-transform pointer-events-none size-4",
                    **{
                        ":class": "{ 'dark:bg-primary-foreground translate-x-[calc(100%-2px)]': checked, 'dark:bg-foreground translate-x-0': !checked }"
                    },
                    aria_hidden=True,
                )()
            ),
        ]

    def __call__(self, *_children: tuple) -> Self:
        warnings.warn(
            f"Trying to add child to a non-child element: {self.__class__.__qualname__}",
            UserWarning,
            stacklevel=2,
        )
        return self
