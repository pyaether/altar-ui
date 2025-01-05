from pytempl.plugins.tailwindcss import tw_merge
from pytempl.tags.html import Div, DivAttributes

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class ProgressBar(Div):
    def __init__(
        self,
        min_value: int,
        max_value: int,
        current_value: int | None = None,
        **attributes: Unpack[DivAttributes],
    ):
        base_class_attribute = (
            "h-2 flex w-full overflow-hidden rounded-full bg-gray-200 dark:bg-gray-800"
        )
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(class_attribute, base_class_attribute),
            x_data=f"{{ currentValue: {current_value if current_value else min_value}, minValue: {min_value}, maxValue: {max_value}, calcPercentage(min, max, val){{return ((val-min)/(max-min))*100}} }}",
            role="progressbar",
            aria_label="Progress Bar",
            **{
                ":aria-valuenow": "currentValue",
                ":aria-valuemin": "minValue",
                ":aria-valuemax": "maxValue",
                "@update.window": "currentValue = $event.detail",
            },
            **attributes,
        )

        self.children.append(
            Div(
                _class="h-full bg-green-500 rounded-full",
                **{
                    ":style": "`width: ${calcPercentage(minValue, maxValue, currentValue)}%`"
                },
            )
        )
