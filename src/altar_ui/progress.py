import warnings
from typing import Self

from aether.plugins.alpinejs import AlpineJSData, Statement, alpine_js_data_merge
from aether.plugins.tailwindcss import tw_merge
from aether.tags.html import Div, DivAttributes

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack  # noqa: UP035


class Progress(Div):
    def __init__(
        self,
        min_value: int,
        max_value: int,
        current_value: int | None = None,
        **attributes: Unpack[DivAttributes],
    ):
        base_class_attribute = (
            "bg-primary/20 relative h-2 w-full overflow-hidden rounded-full"
        )
        base_x_data_attribute = AlpineJSData(
            data={
                "currentValue": current_value if current_value else min_value,
                "minValue": min_value,
                "maxValue": max_value,
                "calcPercentage(min, max, val)": Statement(
                    "{ return ((val-min)/(max-min))*100 }", seq_type="definition"
                ),
            },
            directive="x-data",
        )
        class_attribute = attributes.pop("_class", "")
        x_data_attribute = attributes.pop("x_data", None)

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            x_data=alpine_js_data_merge(base_x_data_attribute, x_data_attribute),
            role="progressbar",
            data_slot="progress",
            **attributes,
        )

        self.children.append(
            Div(
                _class="flex-1 w-full h-full bg-primary transition-all",
                data_slot="progress-indicator",
                **{
                    ":style": "{ transform: `translateX(-${100 - calcPercentage(minValue, maxValue, currentValue)}%)` }"
                },
            )
        )

    def __call__(self, *_children: tuple) -> Self:
        warnings.warn(
            f"Trying to add child to a non-child element: {self.__class__.__qualname__}",
            UserWarning,
            stacklevel=2,
        )

        return self
