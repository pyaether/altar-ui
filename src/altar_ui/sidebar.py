"""Sidebar

A composable, themeable and customizable sidebar component.

Composition:
    Use the following composition to build a Sidebar:

    .
    ├── Sidebar
    │   └── SidebarPanel
    │       ├── SidebarHeader
    │       ├── SidebarSection
    │       │   └── SidebarGroup
    │       │       ├── SidebarGroupLabel
    │       │       └── SidebarList
    │       │           └── SidebarItem
    │       │               ├── SidebarItemButton
    │       │               └── SidebarItemCollapsible
    │       │                   ├── SidebarItemCollapsibleTrigger
    │       │                   └── SidebarList(nested=True)
    │       ├── SidebarSeparator (optional)
    │       └── SidebarFooter (optional)
    └── SidebarMain
        └── SidebarToggle
"""

import json
from enum import StrEnum
from typing import Literal, Self

from aether.plugins.alpinejs import AlpineJSData, Statement, alpine_js_data_merge
from aether.plugins.tailwindcss import tw_merge
from aether.tags.html import (
    H3,
    Aside,
    AsideAttributes,
    Details,
    DetailsAttributes,
    Div,
    DivAttributes,
    Footer,
    FooterAttributes,
    HAttributes,
    Header,
    HeaderAttributes,
    Hr,
    HrAttributes,
    Li,
    LiAttributes,
    Main,
    MainAttributes,
    Nav,
    NavAttributes,
    Section,
    SectionAttributes,
    Summary,
    SummaryAttributes,
    Ul,
    UlAttributes,
)
from aether.tags.html import Button as PyButton
from aether.tags.html import ButtonAttributes as PyButtonAttributes
from altar_icons import ChevronDownIcon, PanelLeftIcon

from .button import Button
from .mixins import AsChildMixin

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack  # noqa: UP035


class SidebarPanelPosition(StrEnum):
    left = "left-0 border-r group-aria-hidden:-translate-x-full"
    right = "right-0 border-l group-aria-hidden:translate-x-full"


class SidebarMainPosition(StrEnum):
    left = "md:ml-[var(--sidebar-width)] peer-aria-hidden:md:ml-0"
    right = "md:mr-[var(--sidebar-width)] peer-aria-hidden:md:mr-0"


class SidebarItemButtonVariant(StrEnum):
    default = "hover:bg-sidebar-accent hover:text-sidebar-accent-foreground"
    outline = "bg-background shadow-[0_0_0_1px_hsl(var(--sidebar-border))] hover:bg-sidebar-accent hover:text-sidebar-accent-foreground hover:shadow-[0_0_0_1px_hsl(var(--sidebar-accent))]"


class SidebarItemButtonSize(StrEnum):
    default = "h-8 text-sm"
    sm = "h-7 text-xs"
    lg = "h-12 text-sm group-data-[collapsible=icon]:!p-0"


class Sidebar(Aside):
    def __init__(
        self,
        default_open: bool = True,
        default_mobile_open: bool = False,
        breakpoint: int = 768,
        **attributes: Unpack[AsideAttributes],
    ):
        base_x_data_attribute = AlpineJSData(
            data={
                "open": False,
                "isMobile": False,
                "breakpoint": breakpoint,
                "_initialMobileOpen": default_mobile_open,
                "_initialOpen": default_open,
                "_mql": None,
                "_mqlListener": None,
                "toggleSidebar(state)": Statement(
                    r"""{
                        const newState = typeof state === 'boolean' ? state : !this.open;
                        if (this.open === newState) return;

                        if (!newState && this.$el.contains(document.activeElement)) {
                            document.activeElement.blur();
                        }

                        this.open = newState;

                    }""",
                    seq_type="definition",
                ),
                "init()": Statement(
                    r"""{
                        this._mql = window.matchMedia(`(max-width: ${this.breakpoint - 1}px)`);
                        this.isMobile = this._mql.matches;

                        this.open = this.isMobile ? this._initialMobileOpen : this._initialOpen;

                        this._mqlListener = (event) => {
                            this.isMobile = event.matches;

                            if (this.isMobile && this.$el.contains(document.activeElement)) {
                                document.activeElement.blur();
                            }

                            this.open = this.isMobile ? false : this._initialOpen;
                        };
                        this._mql.addEventListener('change', this._mqlListener);
                    }""",
                    seq_type="definition",
                ),
                "destroy()": Statement(
                    r"{ if (this._mql && this._mqlListener) { this._mql.removeEventListener('change', this._mqlListener); } }",
                    seq_type="definition",
                ),
            },
            directive="x-data",
        )

        base_class_attribute = "transition-colors peer group max-md:inset-0 max-md:fixed max-md:bg-black/50 max-md:z-40 aria-hidden:max-md:pointer-events-none aria-hidden:max-md:bg-transparent"

        class_attribute = attributes.pop("_class", "")
        x_data_attribute = attributes.pop("x_data", None)

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            x_data=alpine_js_data_merge(base_x_data_attribute, x_data_attribute),
            x_cloak=True,
            **{
                ":aria-hidden": "!open",
                ":inert": "!open || undefined",
                "@altar:sidebar.document": "if (!$event.detail?.id || $event.detail.id === $el.id) { if ($event.detail?.action === 'open') toggleSidebar(true); else if ($event.detail?.action === 'close') toggleSidebar(false); else toggleSidebar(); }",
                "@click.self": "if (isMobile) toggleSidebar(false);",
                "@click": "if (!isMobile) return; if ($event.target.closest('a, button') && !$event.target.closest('[data-keep-sidebar-open]')) { toggleSidebar(false); }",
            },
            **attributes,
        )


class SidebarPanel(Nav):
    def __init__(
        self,
        position: Literal["left", "right"] = "left",
        **attributes: Unpack[NavAttributes],
    ):
        base_class_attribute = "transition-transform duration-300 flex-col inset-y-0 text-sidebar-foreground ease-in-out fixed flex bg-sidebar w-[var(--sidebar-mobile-width)] z-50 md:w-[var(--sidebar-width)]"
        position_class_attribute = SidebarPanelPosition[position]

        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(
                position_class_attribute, base_class_attribute, class_attribute
            ),
            **attributes,
        )


class SidebarHeader(Header):
    def __init__(self, **attributes: Unpack[HeaderAttributes]):
        base_class_attribute = "flex-col gap-2 flex p-2"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            **attributes,
        )


class SidebarSection(Section):
    def __init__(self, **attributes: Unpack[SectionAttributes]):
        base_class_attribute = "overflow-y-auto flex-col min-h-0 flex-1 gap-2 flex"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            **attributes,
        )


class SidebarGroup(Div):
    def __init__(self, **attributes: Unpack[DivAttributes]):
        base_class_attribute = "flex-col relative min-w-0 flex w-full p-2"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            role="group",
            **attributes,
        )


class SidebarGroupLabel(H3):
    def __init__(self, **attributes: Unpack[HAttributes]):
        base_class_attribute = "outline-hidden transition-[margin,opacity] duration-200 rounded-md shrink-0 items-center font-medium text-sidebar-foreground/70 text-xs ring-sidebar-ring ease-linear flex px-2 h-8 focus-visible:ring-2 [&>svg]:shrink-0 [&>svg]:size-4"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            role="heading",
            **attributes,
        )


class SidebarList(Ul):
    def __init__(self, nested: bool = False, **attributes: Unpack[UlAttributes]):
        if nested:
            base_class_attribute = "translate-x-px flex-col border-sidebar-border border-l min-w-0 gap-1 flex px-2.5 py-0.5 w-full"
        else:
            base_class_attribute = "flex-col min-w-0 gap-1 flex w-full"

        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            **attributes,
        )


class SidebarItem(Li):
    def __init__(self, **attributes: Unpack[LiAttributes]):
        base_class_attribute = "relative"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            **attributes,
        )


class SidebarItemButton(AsChildMixin, PyButton):
    def __init__(
        self,
        variant: Literal["default", "outline"] = "default",
        size: Literal["default", "sm", "lg"] = "default",
        current: bool = False,
        as_child: bool = False,
        **attributes: Unpack[PyButtonAttributes],
    ):
        base_class_attribute = "outline-hidden transition-[width,height,padding] overflow-hidden rounded-md items-center text-left ring-sidebar-ring gap-2 flex w-full p-2 aria-disabled:pointer-events-none aria-disabled:opacity-50 aria-[current=page]:font-medium aria-[current=page]:text-sidebar-accent-foreground aria-[current=page]:bg-sidebar-accent focus-visible:ring-2 active:text-sidebar-accent-foreground active:bg-sidebar-accent disabled:pointer-events-none disabled:opacity-50 [&>span:last-child]:truncate [&>svg]:shrink-0 [&>svg]:size-4"
        variant_class_attribute = SidebarItemButtonVariant[variant]
        size_class_attribute = SidebarItemButtonSize[size]
        class_attribute = attributes.pop("_class", "")

        self.as_child = as_child

        super().__init__(
            _class=tw_merge(
                variant_class_attribute,
                size_class_attribute,
                base_class_attribute,
                class_attribute,
            ),
            aria_current="page" if current else None,
            **attributes,
        )


class SidebarItemCollapsible(Details):
    def __init__(self, **attributes: Unpack[DetailsAttributes]):
        closed_state_class_attributes = "[&::details-content]:[block-size:0] [&::details-content]:block [&::details-content]:opacity-0 [&::details-content]:transition-discrete [&::details-content]:transition-all"
        open_state_class_attributes = "open:[&::details-content]:[block-size:auto] open:[&::details-content]:[block-size:calc-size(auto,size)] open:[&::details-content]:opacity-100"

        base_class_attribute = "group [&::details-content]:px-3.5"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(
                closed_state_class_attributes,
                open_state_class_attributes,
                base_class_attribute,
                class_attribute,
            ),
            **attributes,
        )


class SidebarItemCollapsibleTrigger(Summary):
    def __init__(
        self,
        variant: Literal["default", "outline"] = "default",
        size: Literal["default", "sm", "lg"] = "default",
        **attributes: Unpack[SummaryAttributes],
    ):
        base_class_attribute = "outline-hidden transition-[width,height,padding] overflow-hidden rounded-md cursor-pointer items-center text-left ring-sidebar-ring list-none gap-2 flex w-full p-2 aria-disabled:pointer-events-none aria-disabled:opacity-50 aria-[current=page]:font-medium aria-[current=page]:text-sidebar-accent-foreground aria-[current=page]:bg-sidebar-accent focus-visible:ring-2 active:text-sidebar-accent-foreground active:bg-sidebar-accent disabled:pointer-events-none disabled:opacity-50 [&>span:last-child]:truncate [&::-webkit-details-marker]:hidden [&>svg]:shrink-0 [&>svg]:size-4"

        variant_class_attribute = SidebarItemButtonVariant[variant]
        size_class_attribute = SidebarItemButtonSize[size]
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(
                variant_class_attribute,
                size_class_attribute,
                base_class_attribute,
                class_attribute,
            ),
            **attributes,
        )

    def __call__(self, *children: tuple) -> Self:
        super().__call__(*children)

        self.children.append(
            ChevronDownIcon(
                _class="pointer-events-none transition-transform duration-200 shrink-0 text-muted-foreground size-4 ml-auto group-open:rotate-180"
            )
        )

        return self


class SidebarFooter(Footer):
    def __init__(self, **attributes: Unpack[FooterAttributes]):
        base_class_attribute = "flex-col gap-2 flex p-2"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            **attributes,
        )


class SidebarSeparator(Hr):
    def __init__(self, **attributes: Unpack[HrAttributes]):
        base_class_attribute = "border-sidebar-border mx-2 w-auto"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            role="separator",
            **attributes,
        )


class SidebarMain(Main):
    def __init__(
        self,
        position: Literal["left", "right"] = "left",
        **attributes: Unpack[MainAttributes],
    ):
        base_class_attribute = "transition-[margin] duration-300 relative ease-in-out"
        position_class_attribute = SidebarMainPosition[position]

        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(
                position_class_attribute, base_class_attribute, class_attribute
            ),
            **attributes,
        )


class SidebarToggle(Button):
    def __init__(
        self,
        target_id: str | None = None,
        action: Literal["open", "close"] | None = None,
        **attributes: Unpack[PyButtonAttributes],
    ):
        detail = {}
        if target_id:
            detail["id"] = target_id
        if action:
            detail["action"] = action

        if detail:
            options = f"{{ detail: JSON.parse('{json.dumps(detail)}') }}"
            dispatch = (
                f"document.dispatchEvent(new CustomEvent('altar:sidebar', {options}))"
            )
        else:
            dispatch = "document.dispatchEvent(new CustomEvent('altar:sidebar'))"

        super().__init__(
            type="button",
            variant="ghost",
            size="icon",
            **{"@click": dispatch},
            **attributes,
        )

        self.children.append(PanelLeftIcon())
