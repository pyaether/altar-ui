from typing import Any, Dict

from pytempl.plugins.tailwindcss import tw_merge
from pytempl.tags import Button, Div, Input, Span


class Switch(Div):
    def __init__(
        self,
        id: str,
        checked: bool = False,
        disabled: bool = False,
        **attributes: Dict[str, Any],
    ):
        class_attribute = "relative flex items-center"

        forwarded_base_class_attribute = "cursor-pointer h-5 w-9 shrink-0 rounded-full border-2 border-transparent shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-background disabled:cursor-not-allowed disabled:opacity-50"
        forwarded_class_attribute = attributes.pop("_class", "")
        forwarded_attributes = attributes

        super().__init__(
            _class=class_attribute,
            x_data=f"{{ checked: {str(checked).lower()} }}",
        )

        self.children = [
            Button(
                type="button",
                disabled=disabled,
                _class=tw_merge(
                    forwarded_class_attribute, forwarded_base_class_attribute
                ),
                **{
                    "@click": "checked =! checked",
                    ":class": "checked ? 'bg-primary' : 'bg-input'",
                },
                **forwarded_attributes,
            )(
                Span(
                    _class="pointer-events-none h-4 w-4 block rounded-full bg-background shadow-lg ring-0 transition-transform",
                    **{":class": "checked ? 'translate-x-4' : 'translate-x-0'"},
                    aria_hidden=True,
                )()
            ),
            Input(
                id=id,
                _class="sr-only",
                type="checkbox",
                x_model="checked",
                disabled=disabled,
            ),
        ]
