"""Dropdown Menu

Displays a menu to the user, such as a set of actions or functions — triggered by a button.

Composition:
    Use the following composition to build a Dropdown Menu:

    DropdownMenu
    ├── DropdownMenuTrigger
    └── DropdownMenuContent
        └── DropdownMenuMenu
            ├── DropdownMenuGroup (optional)
            │   ├── DropdownMenuGroupLabel (optional)
            │   ├── DropdownMenuItem
            │   │   └── DropdownMenuShortcut (optional)
            │   ├── DropdownMenuCheckboxItem
            │   │   └── DropdownMenuShortcut (optional)
            │   └── DropdownMenuRadioGroup
            │       └── DropdownMenuRadioItem
            │           └── DropdownMenuShortcut (optional)
            ├── DropdownMenuItem
            └── DropdownMenuSeparator(optional)

Requires:
    AlpineJS Focus Plugin (x-trap on PopoverContent)
"""

from typing import Literal, Self

from aether.plugins.alpinejs import AlpineJSData, Statement, alpine_js_data_merge
from aether.plugins.tailwindcss import tw_merge
from aether.tags.html import (
    H3,
    Div,
    DivAttributes,
    HAttributes,
    Hr,
    HrAttributes,
    Span,
    SpanAttributes,
)
from aether.tags.html import (
    ButtonAttributes as PyButtonAttributes,
)
from altar_icons import CheckIcon, DotFilledIcon

from .mixins import AsChildMixin
from .popover import Popover, PopoverContent, PopoverTrigger

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack  # noqa: UP035


class DropdownMenu(Popover):
    def __init__(
        self, default_id: str | None = None, **attributes: Unpack[DivAttributes]
    ):
        if default_id is None:
            default_id = ""

        base_x_data_attribute = AlpineJSData(
            data={
                "isOpen": False,
                "currentItem": default_id,
                "activeId": "",
                "menuId": Statement("$id('dropdown-menu')", seq_type="assignment"),
                "_visibleItems()": Statement(
                    r"""{ return [ ...(this.$refs.menu?.querySelectorAll('[role^="menuitem"]:not([aria-disabled="true"]):not([aria-hidden="true"])') || []) ]; }""",
                    seq_type="definition",
                ),
                "openPopover()": Statement(
                    r"""{
                        this.isOpen = true;
                        this.$nextTick(() => {
                            if (this.$refs.menu) { this.$refs.menu.focus(); }

                            const selected = this.$refs.menu?.querySelector('[aria-selected="true"]');
                        if (selected) {
                                selected.scrollIntoView({ block: 'nearest' });
                                this.activeId= selected.id;
                            } else {
                                const first = this._visibleItems()[0];
                                if (first) this.activeId = first.id;
                            }
                        });
                    }""",
                    seq_type="definition",
                ),
                "closePopover(focusOnTrigger)": Statement(
                    r"""{
                        if (!this.isOpen) return;

                        this.isOpen = false;
                        this.activeId = '';

                        if (focusOnTrigger) this.$refs.trigger?.focus();
                    }""",
                    seq_type="definition",
                ),
                "togglePopoverState()": Statement(
                    "{ this.isOpen ? this.closePopover(true) : this.openPopover(); }",
                    seq_type="definition",
                ),
                "selectItem(id)": Statement(
                    r"{ this.currentItem = id; this.closePopover(true); }",
                    seq_type="definition",
                ),
                "focusNext()": Statement(
                    r"""{
                        const items = this._visibleItems();
                        if (!items.length) return;

                        const current = items.findIndex(i => i.id === this.activeId);
                        const next = items[current < items.length - 1 ? current + 1 : 0];

                        this.activeId = next.id;
                        this.$nextTick(() => next.scrollIntoView({ block: 'nearest' }));
                    }""",
                    seq_type="definition",
                ),
                "focusPrev()": Statement(
                    r"""{
                        const items = this._visibleItems();
                        if (!items.length) return;

                        const current = items.findIndex(i => i.id === this.activeId);
                        const previous = items[current  > 0 ? current - 1 : items.length - 1];

                        this.activeId = previous.id;
                        this.$nextTick(() => previous.scrollIntoView({ block: 'nearest' }));
                    }""",
                    seq_type="definition",
                ),
                "selectActive()": Statement(
                    r"""{
                        if (this.activeId) {
                            const active = this._visibleItems().find(i => i.id === this.activeId);
                            if (active) active.click();
                        }
                    }""",
                    seq_type="definition",
                ),
            },
            directive="x-data",
        )
        x_data_attribute = attributes.pop("x_data", None)

        super().__init__(
            x_data=alpine_js_data_merge(base_x_data_attribute, x_data_attribute),
            data_slot="dropdown-menu",
            **attributes,
        )


class DropdownMenuTrigger(PopoverTrigger):
    def __init__(
        self,
        variant: Literal[
            "default", "destructive", "outline", "secondary", "ghost", "link"
        ] = "outline",
        size: Literal["default", "sm", "lg", "icon", "icon_sm", "icon_lg"] = "default",
        **attributes: Unpack[PyButtonAttributes],
    ):
        base_class_attribute = "font-normal [&>span]:line-clamp-1"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            variant=variant,
            size=size,
            **{
                ":aria-controls": "menuId",
                "aria-haspopup": "menu",
                "@keydown.down.prevent": "if (!isOpen) openPopover()",
                "@keydown.up.prevent": "if (!isOpen) openPopover()",
            },
            **attributes,
        )


class DropdownMenuContent(PopoverContent):
    def __init__(
        self,
        position: Literal["top", "bottom", "left", "right"],
        alignment: Literal["start", "center", "end"] = "start",
        **attributes: Unpack[DivAttributes],
    ):
        base_class_attribute = "min-w-[anchor-size(width)] p-1"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            position=position,
            alignment=alignment,
            **{
                "@keydown.down.prevent": "focusNext()",
                "@keydown.up.prevent": "focusPrev()",
                "@keydown.enter.prevent": "selectActive()",
            },
            **attributes,
        )


class DropdownMenuMenu(Div):
    def __init__(self, **attributes: Unpack[DivAttributes]):
        base_class_attribute = "outline-hidden"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            role="menu",
            x_ref="menu",
            tabindex="-1",
            **{":id": "menuId", "@mousemove": "activeId = ''"},
            **attributes,
        )


class DropdownMenuGroup(Div):
    def __init__(self, **attributes: Unpack[DivAttributes]):
        super().__init__(role="group", **attributes)


class DropdownMenuGroupLabel(H3):
    def __init__(self, **attributes: Unpack[HAttributes]):
        base_class_attribute = "font-medium text-sm flex px-2 py-1.5"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            role="heading",
            **attributes,
        )


class DropdownMenuItem(AsChildMixin, Div):
    def __init__(
        self,
        disabled: bool = False,
        as_child: bool = False,
        **attributes: Unpack[DivAttributes],
    ):
        base_class_attribute = "outline-hidden truncate relative rounded-sm cursor-default select-none items-center text-sm gap-2 flex px-2 py-1.5 w-full group aria-disabled:pointer-events-none aria-disabled:opacity-50 aria-hidden:hidden hover:text-accent-foreground hover:bg-accent disabled:pointer-events-none disabled:opacity-50 [&_svg]:shrink-0 [&_svg]:text-muted-foreground [&.active]:text-accent-foreground [&_svg:not([class*='size-'])]:size-4 [&.active]:bg-accent [&:not([aria-disabled=true])]:focus-visible:text-accent-foreground [&:not([aria-disabled=true])]:focus-visible:bg-accent"
        class_attribute = attributes.pop("_class", "")

        self.as_child = as_child

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            role="menuitem",
            aria_disabled="true" if disabled else "false",
            **{
                ":id": "$id('dropdown-item')",
                "@click": "selectItem($el.id)",
                ":aria-selected": "currentItem === $el.id",
                ":class": "{ 'active': activeId === $el.id }",
            },
            **attributes,
        )


class DropdownMenuCheckboxItem(AsChildMixin, Div):
    def __init__(
        self,
        checked: bool = False,
        disabled: bool = False,
        as_child: bool = False,
        **attributes: Unpack[DivAttributes],
    ):
        base_x_data_attribute = AlpineJSData(
            data={"checked": checked}, directive="x-data"
        )
        base_class_attribute = "outline-hidden truncate relative rounded-sm cursor-default select-none items-center text-sm gap-2 flex px-2 py-1.5 w-full group aria-disabled:pointer-events-none aria-disabled:opacity-50 aria-hidden:hidden hover:text-accent-foreground hover:bg-accent disabled:pointer-events-none disabled:opacity-50 [&_svg]:shrink-0 [&_svg]:text-muted-foreground [&.active]:text-accent-foreground [&_svg]:size-4 [&.active]:bg-accent [&:not([aria-disabled=true])]:focus-visible:text-accent-foreground [&:not([aria-disabled=true])]:focus-visible:bg-accent"
        class_attribute = attributes.pop("_class", "")
        x_data_attribute = attributes.pop("x_data", None)

        self.as_child = as_child

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            x_data=alpine_js_data_merge(base_x_data_attribute, x_data_attribute),
            role="menuitemcheckbox",
            aria_disabled="true" if disabled else "false",
            **{
                ":id": "$id('dropdown-item')",
                "@click": "checked = !checked",
                ":aria-checked": "checked",
                ":class": "{ 'active': activeId === $el.id }",
            },
            **attributes,
        )

    def __call__(self, *children: tuple) -> Self:
        super().__call__(*children)

        self.children.insert(
            0,
            CheckIcon(
                _class="transition-opacity duration-200 opacity-0 size-4 group-aria-checked:opacity-100",
            ),
        )
        return self


class DropdownMenuRadioGroup(Div):
    def __init__(
        self, default_value: str | None = None, **attributes: Unpack[DivAttributes]
    ):
        base_x_data_attribute = AlpineJSData(
            data={"radioValue": default_value or ""}, directive="x-data"
        )
        x_data_attribute = attributes.pop("x_data", None)

        super().__init__(
            role="group",
            x_data=alpine_js_data_merge(base_x_data_attribute, x_data_attribute),
            **attributes,
        )


class DropdownMenuRadioItem(AsChildMixin, Div):
    def __init__(
        self,
        value: str,
        disabled: bool = False,
        as_child: bool = False,
        **attributes: Unpack[DivAttributes],
    ):
        base_class_attribute = "outline-hidden truncate relative rounded-sm cursor-default select-none items-center text-sm gap-2 flex px-2 py-1.5 w-full group aria-disabled:pointer-events-none aria-disabled:opacity-50 aria-hidden:hidden hover:text-accent-foreground hover:bg-accent disabled:pointer-events-none disabled:opacity-50 [&_svg]:shrink-0 [&_svg]:text-muted-foreground [&.active]:text-accent-foreground [&_svg]:size-4 [&.active]:bg-accent [&:not([aria-disabled=true])]:focus-visible:text-accent-foreground [&:not([aria-disabled=true])]:focus-visible:bg-accent"
        class_attribute = attributes.pop("_class", "")

        self.as_child = as_child

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            role="menuitemradio",
            data_value=value,
            aria_disabled="true" if disabled else "false",
            **{
                ":id": "$id('dropdown-item')",
                "@click": "radioValue = $el.dataset.value; closePopover(true);",
                ":aria-checked": "radioValue === $el.dataset.value",
                ":class": "{ 'active': activeId === $el.id }",
            },
            **attributes,
        )

    def __call__(self, *children: tuple) -> Self:
        super().__call__(*children)

        self.children.insert(
            0,
            DotFilledIcon(
                _class="transition-opacity duration-200 opacity-0 size-4 group-aria-checked:opacity-100",
            ),
        )
        return self


class DropdownMenuSeparator(Hr):
    def __init__(self, **attributes: Unpack[HrAttributes]):
        base_class_attribute = "border-border my-1 -mx-1"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            role="separator",
            **attributes,
        )


class DropdownMenuShortcut(Span):
    def __init__(self, **attributes: Unpack[SpanAttributes]):
        base_class_attribute = "tracking-widest text-muted-foreground text-xs ml-auto"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute), **attributes
        )
