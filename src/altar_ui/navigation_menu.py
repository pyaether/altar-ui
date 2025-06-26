from typing import Self

from aether.plugins.alpinejs import AlpineJSData, Statement, alpine_js_data_merge
from aether.plugins.tailwindcss import tw_merge
from aether.tags.html import A, AAttributes, Div, DivAttributes, Nav, NavAttributes
from aether.tags.html import Button as PyButton
from aether.tags.html import ButtonAttributes as PyButtonAttributes
from altar_icons import ChevronDownIcon

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


navigation_menu_trigger_class_attribute = "inline-flex justify-center items-center px-4 py-2 w-max h-9 font-medium text-sm bg-background rounded-md outline-none transition-[color,box-shadow] group disabled:opacity-50 disabled:pointer-events-none hover:text-accent-foreground hover:bg-accent focus:text-accent-foreground focus:bg-accent focus-visible:outline-1 focus-visible:ring-ring/50 focus-visible:ring-[3px]"


class NavigationMenu(Nav):
    def __init__(
        self, enable_mobile_view: bool = False, **attributes: Unpack[NavAttributes]
    ):
        base_class_attribute = (
            "relative flex max-w-max flex-1 items-center justify-center"
        )
        class_attribute = attributes.pop("_class", "")

        if enable_mobile_view:
            base_x_data_attribute = AlpineJSData(
                data={
                    "mobileMenuState": False,
                    "closeMobileMenu()": Statement(
                        "{ this.mobileMenuState = false }",
                        seq_type="definition",
                    ),
                    "toggleMobileMenuState()": Statement(
                        "{ this.mobileMenuState = !this.mobileMenuState }",
                        seq_type="definition",
                    ),
                },
                directive="x-data",
            )
            x_data_attribute = attributes.pop("x_data", None)
            super().__init__(
                data_slot="navigation-menu",
                _class=tw_merge(class_attribute, base_class_attribute),
                x_data=alpine_js_data_merge(base_x_data_attribute, x_data_attribute),
                **{"@click.away": "closeMobileMenu()"},
                **attributes,
            )
        else:
            super().__init__(
                data_slot="navigation-menu",
                _class=tw_merge(class_attribute, base_class_attribute),
                **attributes,
            )


class NavigationMenuList(Div):
    def __init__(self, **attributes: Unpack[DivAttributes]):
        base_class_attribute = (
            "group flex flex-1 list-none items-center justify-center gap-1"
        )
        base_x_data_attribute = AlpineJSData(
            data={
                "selectedNavItem": "",
                "isNavItemActive(value)": Statement(
                    "{ if (this.selectedNavItem === value) { return true } else { return false } }",
                    seq_type="definition",
                ),
                "toggleNavItemActive(value)": Statement(
                    "{ this.selectedNavItem = (this.isNavItemActive(value)) ? '' : value }",
                    seq_type="definition",
                ),
            },
            directive="x-data",
        )
        x_data_attribute = attributes.pop("x_data", None)
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            data_slot="navigation-menu-list",
            _class=tw_merge(class_attribute, base_class_attribute),
            x_data=alpine_js_data_merge(base_x_data_attribute, x_data_attribute),
            **attributes,
        )


class NavigationMenuItem(Div):
    def __init__(self, disabled: bool = False, **attributes: Unpack[DivAttributes]):
        if attributes.get("id"):
            id_attribute = attributes.pop("id")
        elif attributes.get(":id"):
            id_attribute = attributes.pop(":id")
        else:
            id_attribute = "$id('navigation-menu-item')"

        base_class_attribute = "relative"
        base_x_data_attribute = AlpineJSData(
            data={
                "item_disabled": disabled,
                "item_id": Statement(content=id_attribute, seq_type="assignment")
                if "$id" in id_attribute
                else id_attribute.lower().replace(" ", "-"),
            },
            directive="x-data",
        )
        x_data_attribute = attributes.pop("x_data", None)
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            data_slot="navigation-menu-item",
            x_data=alpine_js_data_merge(base_x_data_attribute, x_data_attribute),
            _class=tw_merge(class_attribute, base_class_attribute),
            **{":class": "{ 'pointer-events-none opacity-50': item_disabled }"},
            **attributes,
        )


class NavigationMenuTrigger(PyButton):
    def __init__(self, **attributes: Unpack[PyButtonAttributes]):
        base_class_attribute = navigation_menu_trigger_class_attribute
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            data_slot="navigation-menu-trigger",
            _class=tw_merge(class_attribute, base_class_attribute),
            type="button",
            role="navigation-menu",
            **{
                "@click": "toggleNavItemActive(item_id)",
                ":class": "{ 'hover:bg-accent text-accent-foreground focus:bg-accent bg-accent/50': isNavItemActive(item_id) }",
                ":disabled": "item_disabled",
            },
            **attributes,
        )

    def __call__(self, *children: tuple) -> Self:
        super().__call__(*children)

        self.children.append(
            ChevronDownIcon(
                _class="relative top-[1px] ml-1 transition duration-300 size-3",
                aria_hidden="true",
                **{
                    ":class": "{ 'rotate-180': isNavItemActive(item_id) }",
                },
            )
        )

        return self


class NavigationMenuContent(Div):
    def __init__(self, **attributes: Unpack[DivAttributes]):
        base_class_attribute = (
            "absolute top-full left-0 isolate z-50 flex justify-center"
        )
        base_group_class_attribute = "overflow-hidden top-full mt-1.5 text-popover-foreground bg-popover rounded-md border duration-200 shadow **:data-[slot=navigation-menu-link]:focus:ring-0 **:data-[slot=navigation-menu-link]:focus:outline-none"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            data_slot="navigation-menu-content",
            x_show="isNavItemActive(item_id)",
            x_cloak=True,
            x_collapse=True,
            _class=tw_merge(
                class_attribute, f"{base_class_attribute} {base_group_class_attribute}"
            ),
            **{
                "x-transition:enter": "animate-in zoom-in-95 fade-in-0",
                "x-transition:leave": "animate-out zoom-out-95 fade-out-0",
            },
            **attributes,
        )


class NavigationMenuLink(A):
    def __init__(
        self,
        active: bool | None,
        as_trigger: bool = False,
        **attributes: Unpack[AAttributes],
    ):
        if active is None:
            data_active_class_attribute = ""
        else:
            data_active_class_attribute = "data-[active=true]:focus:bg-accent data-[active=true]:hover:bg-accent data-[active=true]:bg-accent/50 data-[active=true]:text-accent-foreground hover:text-accent-foreground hover:bg-accent"

        base_class_attribute = "flex flex-col gap-1 p-2 text-sm rounded-sm outline-none transition-all [&_svg:not([class*='text-'])]:text-muted-foreground [&_svg:not([class*='size-'])]:size-4 focus:text-accent-foreground focus:bg-accent focus-visible:outline-1 focus-visible:ring-ring/50 focus-visible:ring-[3px]"
        base_x_data_attribute = AlpineJSData(
            data={"isActive": active},
            directive="x-data",
        )
        class_attribute = attributes.pop("_class", "")
        x_data_attribute = attributes.pop("x_data", None)

        super().__init__(
            _class=tw_merge(
                class_attribute,
                f"{base_class_attribute} {data_active_class_attribute} {navigation_menu_trigger_class_attribute}",
            )
            if as_trigger
            else tw_merge(
                class_attribute, f"{base_class_attribute} {data_active_class_attribute}"
            ),
            x_data=alpine_js_data_merge(base_x_data_attribute, x_data_attribute),
            **{
                ":aria-current": "isActive ? 'page' : undefined",
                ":data-active": "isActive",
                ":disabled": "item_disabled",
            },
            **attributes,
        )
