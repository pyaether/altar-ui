"""Tabs

Displays a list of options for the user to pick from - triggered by a button.

Composition:
    Use the following composition to build a Tabs:

    Tabs
    ├── TabsList
    │   ├── TabsTrigger
    │   └── TabsTrigger
    ├── TabsContent
    └── TabsContent

Requires:
    AlpineJS Focus Plugin ($focus on TabsList)
"""

import warnings
from collections.abc import Generator, Iterable
from typing import Self

from aether import BaseWebElement
from aether.plugins.alpinejs import AlpineJSData, Statement, alpine_js_data_merge
from aether.plugins.tailwindcss import tw_merge
from aether.tags.html import Button as PyButton
from aether.tags.html import ButtonAttributes as PyButtonAttributes
from aether.tags.html import Div, DivAttributes, Nav, NavAttributes

from .mixins import AsChildMixin

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack  # noqa: UP035


class Tabs(Div):
    def __init__(self, default_value: str, **attributes: Unpack[DivAttributes]):
        base_class_attribute = "flex-col gap-2 flex"
        base_x_data_attribute = AlpineJSData(
            data={
                "selectedTab": default_value,
                "tabGroupId": Statement("$id('tabs')", seq_type="assignment"),
            },
            directive="x-data",
        )
        class_attribute = attributes.pop("_class", "")
        x_data_attribute = attributes.pop("x_data", None)

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            x_data=alpine_js_data_merge(base_x_data_attribute, x_data_attribute),
            **attributes,
        )


class TabsList(Nav):
    def __init__(self, **attributes: Unpack[NavAttributes]):
        base_class_attribute = "inline-flex justify-center rounded-lg items-center text-muted-foreground bg-muted w-fit h-9 p-[3px]"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            role="tablist",
            aria_orientation="horizontal",
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
                if isinstance(child, TabsTrigger):
                    # Check if child has 'value' parameter. If not, warn the user.
                    if not child.attributes.get("value", None):
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


class TabsTrigger(AsChildMixin, PyButton):
    def __init__(
        self,
        value: str,
        as_child: bool = False,
        **attributes: Unpack[PyButtonAttributes],
    ):
        base_class_attribute = "whitespace-nowrap inline-flex transition-[color,box-shadow] justify-center rounded-md border-transparent border items-center font-medium text-sm text-foreground flex-1 gap-1.5 px-2 py-1 h-[calc(100%-1px)] dark:text-muted-foreground aria-selected:shadow-sm aria-selected:bg-background focus-visible:outline-ring focus-visible:outline-1 focus-visible:border-ring focus-visible:ring-[3px] focus-visible:ring-ring/50 disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:shrink-0 [&_svg:not([class*='size-'])]:size-4 dark:aria-selected:border-input dark:aria-selected:text-foreground dark:aria-selected:bg-input/30"
        class_attribute = attributes.pop("_class", "")

        self.as_child = as_child

        safe_value = value.replace(" ", "-")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            value=value,
            type="button",
            role="tab",
            **{
                ":id": f"`${{tabGroupId}}-trigger-{safe_value}`",
                ":aria-controls": f"`${{tabGroupId}}-content-{safe_value}`",
                "@click": f"selectedTab = '{value}'",
                ":aria-selected": f"selectedTab === '{value}'",
                ":tabindex": f"selectedTab === '{value}' ? '0' : '-1'",
                "@focus": f"selectedTab = '{value}'",
            },
            **attributes,
        )


class TabsContent(Div):
    def __init__(self, value: str, **attributes: Unpack[DivAttributes]):
        base_class_attribute = "outline-none flex-1"
        class_attribute = attributes.pop("_class", "")

        safe_value = value.replace(" ", "-")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            x_show=f"selectedTab === '{value}'",
            role="tabpanel",
            tabindex="0",
            **{
                ":id": f"`${{tabGroupId}}-content-{safe_value}`",
                ":aria-labelledby": f"`${{tabGroupId}}-trigger-{safe_value}`",
            },
            **attributes,
        )
