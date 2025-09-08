import warnings
from collections.abc import Generator, Iterable
from enum import StrEnum
from typing import Literal, Self

from aether import BaseWebElement
from aether.plugins.alpinejs import AlpineJSData, Statement, alpine_js_data_merge
from aether.plugins.tailwindcss import tw_merge
from aether.tags.html import (
    Aside,
    AsideAttributes,
    Div,
    DivAttributes,
    Li,
    LiAttributes,
    Main,
    Nav,
    Span,
    Ul,
    UlAttributes,
)
from aether.tags.html import Button as PyButton
from aether.tags.html import (
    ButtonAttributes as PyButtonAttributes,
)
from altar_icons import PanelLeftIcon

from .button import Button
from .passthrough import Passthrough

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack  # noqa: UP035

# Requires Resize plugin


class SidebarProvider(Div):
    def __init__(self, **attributes: Unpack[DivAttributes]):
        base_x_data_attribute = AlpineJSData(
            data={
                "smallScreenViewport": Statement(
                    "window.innerWidth < 768", seq_type="assignment"
                ),
                "isSidebarOpen": True,
                "isSidebarForSmallScreenViewportOpen": False,
                "closeSidebarForSmallScreenViewport()": Statement(
                    "{ this.isSidebarForSmallScreenViewportOpen = false }",
                    seq_type="definition",
                ),
                "getSidebarState()": Statement(
                    "{ return this.isSidebarOpen ? 'expended' : 'collapsed' }",
                    seq_type="definition",
                ),
                "toggleSidebarState()": Statement(
                    """{
                        if (this.smallScreenViewport) {
                            this.isSidebarForSmallScreenViewportOpen = !this.isSidebarForSmallScreenViewportOpen
                        } else {
                            this.isSidebarOpen = !this.isSidebarOpen
                        }
                    }""",
                    seq_type="definition",
                ),
            },
            directive="x-data",
        )
        base_class_attribute = "flex w-full min-h-svh group/sidebar-wrapper has-data-[variant=inset]:bg-sidebar"

        x_data_attribute = attributes.pop("x_data", None)
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            data_slot="sidebar-wrapper",
            _class=tw_merge(base_class_attribute, class_attribute),
            x_data=alpine_js_data_merge(base_x_data_attribute, x_data_attribute),
            **{"x-resize.window": "smallScreenViewport = window.innerWidth < 768"},
            **attributes,
        )

    def __call__(self, *children: BaseWebElement) -> Self:
        allowed_first_child_types = (Sidebar,)
        allowed_second_child_types = (Div, Main)

        if len(children) != 2:
            raise ValueError(
                f"`{self.__class__.__qualname__}` must be called with exactly two children, but got {len(children)}."
            )

        if not isinstance(children[0], allowed_first_child_types):
            raise ValueError(
                f"First element of `{self.__class__.__qualname__}` must be a `{', '.join([type(allowed_type).__class__.__qualname__ for allowed_type in allowed_first_child_types])}`, but got {type(children[0]).__name__} instead."
            )

        if not isinstance(children[1], allowed_second_child_types):
            raise ValueError(
                f"Second element of `{self.__class__.__qualname__}` must be a `{', '.join([type(allowed_type).__class__.__qualname__ for allowed_type in allowed_second_child_types])}`, but got {type(children[1]).__name__} instead."
            )

        return super().__call__(*children)


class SidebarTrigger(Button):
    def __init__(self, **attributes: Unpack[PyButtonAttributes]):
        base_class_attribute = "size-7"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            type="button",
            variant="ghost",
            size="icon",
            data_sidebar="trigger",
            data_slot="sidebar-trigger",
            **{"@click": "toggleSidebarState()"},
            **attributes,
        )

        self.children = [PanelLeftIcon(), Span(_class="sr-only")("Toggle Sidebar")]

    def __call__(self, *_children: tuple) -> Self:
        warnings.warn(
            f"Trying to add child to a non-child element: {self.__class__.__qualname__}",
            UserWarning,
            stacklevel=2,
        )

        return self


class Sidebar(Div):
    def __init__(
        self,
        side: Literal["left", "right"] = "left",
        variant: Literal["sidebar", "floating", "inset"] = "sidebar",
        collapsible: Literal["offcanvas", "icon", "none"] = "offcanvas",
        **attributes: Unpack[AsideAttributes],
    ):
        data_side_class_attribute = (
            "left-0 group-data-[collapsible=offcanvas]:left-[calc(var(--sidebar-width)*-1)]"
            if side == "left"
            else "right-0 group-data-[collapsible=offcanvas]:right-[calc(var(--sidebar-width)*-1)]"
        )
        data_variant_class_attribute = (
            "group-data-[collapsible=icon]:w-[var(--sidebar-width-icon)] group-data-[side=left]:border-r group-data-[side=right]:border-l"
            if variant == "sidebar"
            else "p-2 group-data-[collapsible=icon]:w-[calc(var(--sidebar-width-icon)+(--spacing(4))+2px)]"
        )

        self.forwarded_base_class_attribute = (
            f"{data_side_class_attribute} {data_variant_class_attribute}"
        )
        self.forwarded_class_attribute = attributes.pop("_class", "")

        self.forwarded_attributes = attributes

        super().__init__(
            data_slot="sidebar",
            data_sidebar="sidebar",
            **{
                ":class": "!smallScreenViewport ? 'group peer text-sidebar-foreground hidden md:block' : undefined",
                ":data-state": "!smallScreenViewport ? getSidebarState() : undefined",
                ":data-side": f"!smallScreenViewport ? '{side}' : undefined",
                ":data-variant": f"!smallScreenViewport ? '{variant}' : undefined",
                ":data-collapsible": f"!smallScreenViewport ? (getSidebarState() === 'collapsed' ? '{collapsible}' : '') : undefined",
                ":data-mobile": "smallScreenViewport ? true : undefined",
            },
        )

        self.sidebar_side = side
        self.sidebar_variant = variant

    def __call__(self, *children: tuple) -> Self:
        forwarded_children = []
        for child in children:
            if (
                isinstance(child, str)
                or isinstance(child, BaseWebElement)
                or not isinstance(child, Iterable)
            ):
                forwarded_children.append(child)
            elif isinstance(child, Generator):
                forwarded_children.extend(list(child))
            elif isinstance(child, type(None)):
                continue
            else:
                forwarded_children.extend(child)

        self.children = [
            Div(x_show="smallScreenViewport")(
                Div(x_show="isSidebarForSmallScreenViewportOpen", x_cloak=True)(
                    Div(
                        _class="fixed inset-0 z-40 bg-sidebar-foreground/50 backdrop-blur-sm",
                        x_cloak=True,
                        x_show="isSidebarForSmallScreenViewportOpen",
                        **{
                            "@click": "closeSidebarForSmallScreenViewport()",
                            "x-transition.opacity": True,
                        },
                    )(),
                    Aside(
                        data_slot="sidebar-container",
                        _class=tw_merge(
                            "fixed top-0 bottom-0 z-50 flex h-full w-[var(--sidebar-width)] flex-col border-outline bg-sidebar text-sidebar-foreground p-0 [&>button]:hidden transition-transform duration-300",
                            "left-0 border-r"
                            if self.sidebar_side == "left"
                            else "right-0 border-l",
                        ),
                        **{
                            ":class": f"""{{ 'translate-x-0': isSidebarForSmallScreenViewportOpen, '{"-translate-x-full" if self.sidebar_side == "left" else "translate-x-full"}': !isSidebarForSmallScreenViewportOpen }}"""
                        },
                        **self.forwarded_attributes,
                    )(
                        Div(
                            _class=tw_merge(
                                "flex flex-col w-full h-full",
                                self.forwarded_class_attribute,
                            ),
                            data_sidebar="sidebar",
                            data_slot="sidebar-inner",
                        )(*forwarded_children)
                    ),
                )
            ),
            Div(x_show="!smallScreenViewport")(
                Div()(
                    Div(
                        data_slot="sidebar-gap",
                        _class=tw_merge(
                            "relative w-[var(--sidebar-width)] bg-transparent transition-[width] duration-200 ease-linear group-data-[collapsible=offcanvas]:w-0 group-data-[side=right]:rotate-180",
                            "group-data-[collapsible=icon]:w-[var(--sidebar-width-icon)]"
                            if self.sidebar_variant == "sidebar"
                            else "group-data-[collapsible=icon]:w-[calc(var(--sidebar-width-icon)+(--spacing(4)))]",
                        ),
                    )(),
                    Aside(
                        data_slot="sidebar-container",
                        _class=tw_merge(
                            "fixed inset-y-0 z-10 hidden h-svh w-[var(--sidebar-width)] transition-[left,right,width] duration-200 ease-linear md:flex",
                            self.forwarded_base_class_attribute,
                        ),
                        **self.forwarded_attributes,
                    )(
                        Div(
                            data_sidebar="sidebar",
                            data_slot="sidebar-inner",
                            _class=tw_merge(
                                "flex flex-col w-full h-full bg-sidebar group-data-[variant=floating]:border-sidebar-border group-data-[variant=floating]:rounded-lg group-data-[variant=floating]:border group-data-[variant=floating]:shadow-sm",
                                self.forwarded_class_attribute,
                            ),
                        )(*forwarded_children)
                    ),
                )
            ),
        ]

        return self


class SidebarHeader(Div):
    def __init__(self, **attributes: Unpack[DivAttributes]):
        base_class_attribute = (
            "flex flex-col gap-2 p-2 group-data-[collapsible=icon]:overflow-hidden"
        )
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            data_slot="sidebar-header",
            data_sidebar="header",
            **attributes,
        )


class SidebarContent(Div):
    def __init__(self, **attributes: Unpack[DivAttributes]):
        base_x_data_attribute = AlpineJSData(
            data={"currentActiveMenuItem": None}, directive="x-data"
        )
        base_class_attribute = "flex flex-1 flex-col overflow-auto gap-2 min-h-0 group-data-[collapsible=icon]:overflow-hidden"

        x_data_attribute = attributes.pop("x_data", None)
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            x_data=alpine_js_data_merge(base_x_data_attribute, x_data_attribute),
            data_slot="sidebar-content",
            data_sidebar="content",
            **attributes,
        )


class SidebarFooter(Div):
    def __init__(self, **attributes: Unpack[DivAttributes]):
        base_class_attribute = "flex flex-col gap-2 p-2"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            data_slot="sidebar-footer",
            data_sidebar="footer",
            **attributes,
        )


class SidebarSeparator(Div):
    def __init__(self, **attributes: Unpack[DivAttributes]):
        base_class_attribute = "mx-2 w-auto h-px bg-sidebar-border"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            role="separator",
            aria_orientation="horizontal",
            data_slot="sidebar-separator",
            data_sidebar="separator",
            **attributes,
        )

    def __call__(self, *_children: tuple) -> Self:
        warnings.warn(
            f"Trying to add child to a non-child element: {self.__class__.__qualname__}",
            UserWarning,
            stacklevel=2,
        )
        return self


class SidebarGroup(Div):
    def __init__(self, **attributes: Unpack[DivAttributes]):
        base_class_attribute = "flex flex-col relative p-2 w-full min-w-0"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            data_slot="sidebar-group",
            data_sidebar="group",
            **attributes,
        )


class SidebarGroupLabel(Div):
    def __init__(self, pass_through: bool = False, **attributes: Unpack[DivAttributes]):
        base_class_attribute = "flex items-center px-2 h-8 font-medium text-sidebar-foreground/70 text-xs rounded-md outline-hidden ring-sidebar-ring transition-[margin,opacity] duration-200 ease-linear shrink-0 group-data-[collapsible=icon]:-mt-8 group-data-[collapsible=icon]:opacity-0 focus-visible:ring-2 [&>svg]:size-4 [&>svg]:shrink-0"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            data_slot="sidebar-group-label",
            data_sidebar="group-label",
            **attributes,
        )

        self.pass_through = pass_through

    def __call__(self, *children: tuple) -> Self | Passthrough:
        if self.pass_through:
            return Passthrough(**self.attributes)(*children)
        else:
            return super().__call__(*children)


class SidebarGroupContent(Div):
    def __init__(self, **attributes: Unpack[DivAttributes]):
        base_class_attribute = "w-full text-sm"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            data_slot="sidebar-group-content",
            data_sidebar="group-content",
            **attributes,
        )


class SidebarMenuButtonVariant(StrEnum):
    default = "hover:bg-sidebar-accent hover:text-sidebar-accent-foreground"
    outline = "bg-background shadow-[0_0_0_1px_hsl(var(--sidebar-border))] hover:bg-sidebar-accent hover:text-sidebar-accent-foreground hover:shadow-[0_0_0_1px_hsl(var(--sidebar-accent))]"


class SidebarMenuButtonSize(StrEnum):
    default = "h-8 text-sm group-data-[collapsible=icon]:p-2!"
    sm = "h-7 text-xs group-data-[collapsible=icon]:p-2!"
    lg = "h-12 text-sm group-data-[collapsible=icon]:p-0!"


class SidebarMenu(Nav):
    def __init__(self, **attributes: Unpack[UlAttributes]):
        self.forwarded_base_class_attribute = "flex flex-col gap-1 w-full min-w-0"
        self.forwarded_class_attribute = attributes.pop("_class", "")
        self.forwarded_attributes = attributes

        super().__init__(data_slot="sidebar-navigation", data_sidebar="navigation")

    def __call__(self, *children: tuple) -> Self:
        allowed_child_types = (str, BaseWebElement)

        forwarded_children = []
        for child in children:
            if isinstance(child, allowed_child_types) or not isinstance(
                child, Iterable
            ):
                forwarded_children.append(child)
            elif isinstance(child, Generator):
                forwarded_children.extend(list(child))
            elif isinstance(child, type(None)):
                continue
            else:
                forwarded_children.extend(child)

        self.children.append(
            Ul(
                _class=tw_merge(
                    self.forwarded_base_class_attribute,
                    self.forwarded_class_attribute,
                ),
                data_slot="sidebar-menu",
                data_sidebar="menu",
                **self.forwarded_attributes,
            )(*forwarded_children)
        )

        return self


class SidebarMenuItem(Li):
    def __init__(self, is_active: bool = False, **attributes: Unpack[LiAttributes]):
        if attributes.get("smi_id"):
            smi_id_attribute = attributes.pop("smi_id")
        else:
            smi_id_attribute = "$id('sidebar-menu-item')"

        base_x_data_attribute = AlpineJSData(
            data={
                "sidebarMenuItem": Statement(
                    content=smi_id_attribute, seq_type="assignment"
                ),
                "setActive()": Statement(
                    content="{ currentActiveMenuItem = this.sidebarMenuItem }",
                    seq_type="definition",
                ),
                "isItemActive()": Statement(
                    content="{ if (currentActiveMenuItem === this.sidebarMenuItem) {return true} else {return null} }",
                    seq_type="definition",
                ),
            },
            directive="x-data",
        )
        base_class_attribute = "relative group/menu-item"

        x_data_attribute = attributes.pop("x_data", None)
        class_attribute = attributes.pop("_class", "")

        if is_active:
            x_data_to_set_item_active = AlpineJSData(
                data={
                    "init()": Statement(
                        content="{ currentActiveMenuItem = this.sidebarMenuItem }",
                        seq_type="definition",
                    ),
                },
                directive="x-data",
            )

            base_x_data_attribute = alpine_js_data_merge(
                base_x_data_attribute, x_data_to_set_item_active
            )

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            x_data=alpine_js_data_merge(base_x_data_attribute, x_data_attribute),
            data_slot="sidebar-menu-item",
            data_sidebar="menu-item",
            **attributes,
        )


class SidebarMenuButton(PyButton):
    def __init__(
        self,
        pass_through: bool = False,
        has_active_state: bool = False,
        variant: Literal["default", "outline"] = "default",
        size: Literal["default", "sm", "lg"] = "default",
        **attributes: Unpack[PyButtonAttributes],
    ):
        base_class_attribute = "flex overflow-hidden gap-2 items-center p-2 w-full text-left text-sm rounded-md outline-hidden ring-sidebar-ring transition-[width,height,padding] peer/menu-button group-has-data-[sidebar=menu-action]/menu-item:pr-8 aria-disabled:pointer-events-none aria-disabled:opacity-50 data-[active]:bg-sidebar-accent data-[active]:font-medium data-[active]:text-sidebar-accent-foreground data-[state=open]:hover:bg-sidebar-accent data-[state=open]:hover:text-sidebar-accent-foreground group-data-[collapsible=icon]:size-8! [&>span:last-child]:truncate disabled:opacity-50 disabled:pointer-events-none hover:text-sidebar-accent-foreground hover:bg-sidebar-accent focus-visible:ring-2 active:text-sidebar-accent-foreground active:bg-sidebar-accent [&>svg]:size-4 [&>svg]:shrink-0"

        variant_class_attribute = SidebarMenuButtonVariant[variant]
        size_class_attribute = SidebarMenuButtonSize[size]
        class_attribute = attributes.pop("_class", "")

        data_slot = attributes.pop("data_slot", "sidebar-menu-button")

        super().__init__(
            _class=tw_merge(
                variant_class_attribute,
                size_class_attribute,
                base_class_attribute,
                class_attribute,
            ),
            data_slot=data_slot,
            data_size=size,
            data_sidebar="menu-button",
            **{
                ":data-state": "isSidebarForSmallScreenViewportOpen",
                ":data-active": "isItemActive()" if has_active_state else None,
                "@click": "setActive()" if has_active_state else None,
            },
            **attributes,
        )

        self.pass_through = pass_through

    def __call__(self, *children: tuple) -> Self | Passthrough:
        if self.pass_through:
            return Passthrough(**self.attributes)(*children)
        else:
            return super().__call__(*children)
