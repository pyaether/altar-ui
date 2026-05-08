"""Progress

Displays an indicator showing the completion progress of a task, typically displayed as a progress bar.

Composition:
    Use the following composition to build a Progress:

    Progress
    └── ProgressIndicator
"""

import warnings
from typing import Self

from aether.plugins.tailwindcss import tw_merge
from aether.tags.html import Div, DivAttributes

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack  # noqa: UP035


class Progress(Div):
    def __init__(self, **attributes: Unpack[DivAttributes]):
        base_class_attribute = (
            "bg-primary/20 relative h-2 w-full overflow-hidden rounded-full"
        )
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            role="progressbar",
            **attributes,
        )


class ProgressIndicator(Div):
    def __init__(
        self, value: int | float | None = None, **attributes: Unpack[DivAttributes]
    ):
        base_class_attribute = "transition-all flex-1 bg-primary w-full h-full"
        class_attribute = attributes.pop("_class", "")

        style_attribute = attributes.pop("style", "")
        if value is not None:
            style_attribute = f"width: {value}%; {style_attribute}".strip()

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            style=style_attribute if style_attribute else None,
            **attributes,
        )

    def __call__(self, *_children: tuple) -> Self:
        warnings.warn(
            f"Trying to add child to a non-child element: {self.__class__.__qualname__}",
            UserWarning,
            stacklevel=2,
        )

        return self
