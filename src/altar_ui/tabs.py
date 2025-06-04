import warnings
from collections.abc import Generator, Iterable
from typing import Self

from aether import BaseWebElement
from aether.plugins.alpinejs import AlpineJSData, Statement, alpine_js_data_merge
from aether.plugins.tailwindcss import tw_merge
from aether.tags.html import Button as PyButton
from aether.tags.html import ButtonAttributes as PyButtonAttributes
from aether.tags.html import Div, DivAttributes

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class Tabs(Div):
    def __init__(self, default_value: str, **attributes: Unpack[DivAttributes]):
        base_class_attribute = "flex flex-col gap-2"
        base_x_data_attribute = AlpineJSData(
            data={
                "selectedTab": default_value,
                "isTabActive(value)": Statement(
                    "{ if (this.selectedTab === value) { return true } else { return false } }",
                    seq_type="definition",
                ),
                "setTabActive(value)": Statement(
                    "{ this.selectedTab = value }",
                    seq_type="definition",
                ),
            },
            directive="x-data",
        )
        class_attribute = attributes.pop("_class", "")
        x_data_attribute = attributes.pop("x_data", None)

        super().__init__(
            data_slot="tabs",
            _class=tw_merge(class_attribute, base_class_attribute),
            x_data=alpine_js_data_merge(base_x_data_attribute, x_data_attribute),
            **attributes,
        )


class TabsList(Div):
    def __init__(self, **attributes: Unpack[DivAttributes]):
        base_class_attribute = "bg-muted text-muted-foreground inline-flex h-9 w-fit items-center justify-center rounded-lg p-[3px]"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            data_slot="tabs-list",
            _class=tw_merge(class_attribute, base_class_attribute),
            role="tablist",
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


class TabsTrigger(PyButton):
    def __init__(self, value: str, **attributes: Unpack[PyButtonAttributes]):
        base_class_attribute = "focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:outline-ring text-foreground dark:text-muted-foreground inline-flex h-[calc(100%-1px)] flex-1 items-center justify-center gap-1.5 rounded-md border border-transparent px-2 py-1 text-sm font-medium whitespace-nowrap transition-[color,box-shadow] focus-visible:ring-[3px] focus-visible:outline-1 disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:shrink-0 [&_svg:not([class*='size-'])]:size-4"
        class_attribute = attributes.pop("_class", "")

        if attributes.get("id"):
            id_attribute = attributes.pop("id")
        elif attributes.get(":id"):
            id_attribute = attributes.pop(":id")
        else:
            id_attribute = "$id('tabs-trigger')"

        super().__init__(
            data_slot="tabs-trigger",
            _class=tw_merge(class_attribute, base_class_attribute),
            value=value,
            **{":id": id_attribute}
            if "$id" in id_attribute
            else {"id": f"{id_attribute.lower().replace(' ', '-')}"},
            type="button",
            role="tab",
            **{
                "@click": f"setTabActive('{value}')",
                ":class": f"{{ 'bg-background dark:text-foreground dark:border-input dark:bg-input/30 shadow-sm': isTabActive('{value}')}}",
                ":aria-selected": f"isTabActive('{value}')",
                ":tabindex": f"isTabActive('{value}') ? '0' : '-1'",
            },
            **attributes,
        )


class TabsContent(Div):
    def __init__(self, value: str, **attributes: Unpack[DivAttributes]):
        base_class_attribute = "flex-1 outline-none"
        class_attribute = attributes.pop("_class", "")

        if attributes.get("id"):
            id_attribute = attributes.pop("id")
        elif attributes.get(":id"):
            id_attribute = attributes.pop(":id")
        else:
            id_attribute = "$id('tabs-content')"

        super().__init__(
            data_slot="tabs-content",
            _class=tw_merge(class_attribute, base_class_attribute),
            x_show=f"isTabActive('{value}')",
            **{":id": id_attribute}
            if "$id" in id_attribute
            else {"id": f"{id_attribute.lower().replace(' ', '-')}"},
            role="tabpanel",
            **attributes,
        )
