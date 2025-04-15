import warnings
from collections.abc import Generator, Iterable
from typing import Self

from pytempl import BaseWebElement
from pytempl.plugins.tailwindcss import tw_merge
from pytempl.tags.html import (
    Button,
    Div,
    DivAttributes,
)
from pytempl.tags.html import (
    ButtonAttributes as PyButtonAttributes,
)

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class Tabs(Div):
    def __init__(self, default_value: str, **attributes: Unpack[DivAttributes]):
        super().__init__(
            x_data=f"{{ selectedTab: '{default_value}' }}",
            **attributes,
        )


class TabsList(Div):
    def __init__(self, **attributes: Unpack[DivAttributes]):
        base_class_attribute = "inline-flex h-9 items-center justify-center rounded-lg bg-muted p-1 text-muted-foreground"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(class_attribute, base_class_attribute),
            role="tablist",
            aria_label="tab options",
            **{
                "@keydown.right.prevent": "$focus.wrap().next()",
                "@keydown.left.prevent": "$focus.wrap().previous()",
            },
            **attributes,
        )

    def __call__(self, *children: tuple) -> Self:
        for child in children:
            if (
                isinstance(child, str)
                or isinstance(child, BaseWebElement)
                or not isinstance(child, Iterable)
            ):
                if isinstance(child, BaseWebElement):
                    # Check if child has 'value' parameter. If not, warn the user.
                    tab_value = child.attributes.pop("value", None)
                    if not tab_value:
                        warnings.warn(
                            f"Trying to add child that doesn't have 'value' parameter: {self.__class__.__name__}",
                            UserWarning,
                            stacklevel=2,
                        )
                self.children.append(child)
            elif isinstance(child, Generator):
                self.children.extend(list(child))
            elif isinstance(child, type(None)):
                continue
            else:
                self.children.extend(child)

        return self


class TabsTrigger(Button):
    def __init__(self, value: str, **attributes: Unpack[PyButtonAttributes]):
        base_class_attribute = "inline-flex items-center justify-center whitespace-nowrap rounded-md px-3 py-1 text-sm font-medium ring-offset-background transition-all disabled:pointer-events-none disabled:opacity-50"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(class_attribute, base_class_attribute),
            value=value,
            type="button",
            role="tab",
            aria_controls=f"tabpanel_{value}",
            **{
                "@click": f"selectedTab = '{value}'",
                ":class": f"selectedTab === '{value}' ? 'bg-background text-foreground shadow' : ''; $focus.focused() === '{value}' ? 'outline-none ring-2 ring-ring ring-offset-2' : ''",
                ":aria-selected": f"selectedTab === '{value}'",
                ":tabindex": f"selectedTab === '{value}' ? '0' : '-1'",
            },
            **attributes,
        )


class TabsContent(Div):
    def __init__(self, value: str, **attributes: Unpack[DivAttributes]):
        base_class_attribute = "mt-2 ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(class_attribute, base_class_attribute),
            x_show=f"selectedTab === '{value}'",
            id=f"tabpanel_{value}",
            role="tabpanel",
            aria_label=value,
            **attributes,
        )
