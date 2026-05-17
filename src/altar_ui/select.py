"""Select

Displays a list of options for the user to pick from - triggered by a button.

Composition:
    Use the following composition to build a Select:

    Select
    ├── SelectTrigger
    │   └── SelectValue
    ├── SelectContent
    │   ├── SelectSearch (optional)
    │   └── SelectListbox
    │       ├── SelectGroup (optional)
    │       │   ├── SelectGroupLabel
    │       │   └── SelectItem
    │       ├── SelectItem
    │       └── SelectSeparator (optional)
    └── (hidden input — rendered when `name` is provided)

Requires:
    AlpineJS Focus Plugin (x-trap on PopoverContent)
"""

import warnings
from typing import Literal, Self

from aether.plugins.alpinejs import (
    AlpineHookForm,
    AlpineJSData,
    Statement,
    alpine_js_data_merge,
)
from aether.plugins.tailwindcss import tw_merge
from aether.tags.html import (
    H3,
    Div,
    DivAttributes,
    HAttributes,
    Header,
    Hr,
    HrAttributes,
    Input,
    InputAttributes,
    Span,
    SpanAttributes,
    Template,
)
from aether.tags.html import ButtonAttributes as PyButtonAttributes
from altar_icons import CheckIcon, ChevronsUpDownIcon, SearchIcon

from .badge import Badge
from .form import FormControl
from .popover import Popover, PopoverContent, PopoverTrigger

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack  # noqa: UP035


class Select(Popover):
    def __init__(
        self,
        name: str | None = None,
        default_value: str | list | None = None,
        multiple_select: bool = False,
        placeholder: str = "Select an option...",
        close_on_select: bool = False,
        hook_form_item: AlpineHookForm | None = None,
        **attributes: Unpack[DivAttributes],
    ):
        if default_value is None:
            default_value = [] if multiple_select else ""

        if not multiple_select and isinstance(default_value, list):
            raise ValueError(
                "'default_value' cannot be a list when 'multiple_select = False'"
            )

        if multiple_select and isinstance(default_value, str):
            default_value = [default_value]

        self.forwarded_name_attribute = name
        self.forwarded_hook_form_item = hook_form_item

        base_x_data_attribute = AlpineJSData(
            data={
                "isOpen": False,
                "isMultiple": multiple_select,
                "currentValue": default_value,
                "currentLabels": [] if multiple_select else "",
                "filter": "",
                "activeValue": "",
                "placeholder": placeholder,
                "closeOnSelect": close_on_select,
                "listboxId": Statement("$id('select-listbox')", seq_type="assignment"),
                "init()": Statement(
                    r"""{
                        this.$nextTick(() => {
                            const opts = Array.from(this.$root.querySelectorAll('[role="option"]'));

                            if (this.isMultiple && this.currentValue.length > 0) {
                                const selected = opts.filter(opt => this.currentValue.includes(opt.dataset.value));
                                this.currentLabels = selected.map(opt => opt.dataset.label || opt.textContent.trim());
                            } else if (!this.isMultiple && this.currentValue) {
                                const opt = opts.find(o => o.dataset.value === this.currentValue);
                                if (opt) this.currentLabels = opt.dataset.label || opt.textContent.trim();
                            }
                        });
                    }""",
                    seq_type="definition",
                ),
                "_visibleOptions()": Statement(
                    r"""{ return [ ...(this.$refs.listbox?.querySelectorAll('[role="option"]:not([aria-hidden="true"]):not([aria-disabled="true"])') || []) ]; }""",
                    seq_type="definition",
                ),
                "openPopover()": Statement(
                    r"""{
                        this.isOpen = true;
                        this.$nextTick(() => {
                            if (this.$refs.searchInput) { this.$refs.searchInput.focus(); }
                            else if (this.$refs.listbox) { this.$refs.listbox.focus(); }

                            const selected = this.$refs.listbox?.querySelector('[aria-selected="true"]');
                            if (selected) {
                                selected.scrollIntoView({ block: 'nearest' });
                                this.activeValue = selected.dataset.value;
                            } else {
                                const first = this._visibleOptions()[0];
                                if (first) this.activeValue = first.dataset.value;
                            }
                        });
                    }""",
                    seq_type="definition",
                ),
                "closePopover(focusOnTrigger)": Statement(
                    r"""{
                        if (!this.isOpen) return;

                        this.isOpen = false;
                        this.filter = '';
                        this.activeValue = '';

                        if (focusOnTrigger) this.$refs.trigger?.focus();
                    }""",
                    seq_type="definition",
                ),
                "togglePopoverState()": Statement(
                    "{ this.isOpen ? this.closePopover(true) : this.openPopover(); }",
                    seq_type="definition",
                ),
                "selectValue(value, label)": Statement(
                    r"""{
                        label = label || value;

                        if (this.isMultiple) {
                            const idx = this.currentValue.indexOf(value);
                            if (idx !== -1) {
                                this.currentValue = this.currentValue.filter((_, i) => i !== idx);
                                this.currentLabels = this.currentLabels.filter((_, i) => i !== idx);
                            } else {
                                this.currentValue = [...this.currentValue, value];
                                this.currentLabels = [...this.currentLabels, label];
                            }

                            if (this.closeOnSelect) this.closePopover(true);
                        } else {
                            this.currentValue = value;
                            this.currentLabels = label;
                            this.closePopover(true);
                        }
                    }""",
                    seq_type="definition",
                ),
                "getDisplayLabel()": Statement(
                    r"""{
                        if (this.isMultiple) return this.currentLabels.length ? this.currentLabels.join(', ') : this.placeholder;

                        return this.currentLabels || this.placeholder;
                    }""",
                    seq_type="definition",
                ),
                "matchesFilter(elt)": Statement(
                    r"""{
                        if (!this.filter) return true;

                        if (elt.dataset.force === 'true') return true;

                        const text = (elt.dataset.label || elt.textContent).trim().toLowerCase();
                        const keywords = (elt.dataset.keywords || '').toLowerCase();
                        const query = this.filter.toLowerCase();

                        return text.includes(query) || keywords.includes(query);
                    }""",
                    seq_type="definition",
                ),
                "focusNext()": Statement(
                    r"""{
                        const opts = this._visibleOptions();
                        if (!opts.length) return;

                        const current = opts.findIndex(o => o.dataset.value === this.activeValue);
                        const next = opts[current < opts.length - 1 ? current + 1 : 0];

                        this.activeValue = next.dataset.value;
                        this.$nextTick(() => next.scrollIntoView({ block: 'nearest' }));
                    }""",
                    seq_type="definition",
                ),
                "focusPrev()": Statement(
                    r"""{
                        const opts = this._visibleOptions();
                        if (!opts.length) return;

                        const current = opts.findIndex(o => o.dataset.value === this.activeValue);
                        const previous = opts[current  > 0 ? current - 1 : opts.length - 1];

                        this.activeValue = previous.dataset.value;
                        this.$nextTick(() => previous.scrollIntoView({ block: 'nearest' }));

                    }""",
                    seq_type="definition",
                ),
                "selectActive()": Statement(
                    r"{ if (this.activeValue) { this._visibleOptions().find(o => o.dataset.value === this.activeValue)?.click(); } }",
                    seq_type="definition",
                ),
            },
            directive="x-data",
        )
        x_data_attribute = attributes.pop("x_data", None)

        super().__init__(
            x_data=alpine_js_data_merge(base_x_data_attribute, x_data_attribute),
            data_slot="select",
            **attributes,
        )

    def __call__(self, *children: tuple) -> Self:
        super().__call__(*children)

        if self.forwarded_hook_form_item or self.forwarded_name_attribute:
            self.children.append(
                Input(
                    type="hidden",
                    name=self.forwarded_name_attribute,
                    **{
                        ":value": "isMultiple ? JSON.stringify(currentValue) : currentValue"
                    },
                )
                if self.forwarded_name_attribute
                else FormControl(hook_form_item=self.forwarded_hook_form_item)(
                    Input(
                        type="hidden",
                        **{
                            ":value": "isMultiple ? JSON.stringify(currentValue) : currentValue"
                        },
                    )
                )
            )

        return self


class SelectTrigger(PopoverTrigger):
    def __init__(
        self,
        variant: Literal[
            "default", "destructive", "outline", "secondary", "ghost", "link"
        ] = "outline",
        size: Literal["default", "sm", "lg", "icon", "icon_sm", "icon_lg"] = "default",
        **attributes: Unpack[PyButtonAttributes],
    ):
        base_class_attribute = "justify-between font-normal aria-invalid:border-destructive aria-invalid:ring-destructive/20 [&>span]:line-clamp-1 dark:aria-invalid:ring-destructive/40"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            variant=variant,
            size=size,
            **{
                ":aria-controls": "listboxId",
                "aria-haspopup": "listbox",
                "@keydown.down.prevent": "if (!isOpen) openPopover()",
                "@keydown.up.prevent": "if (!isOpen) openPopover()",
            },
            **attributes,
        )

    def __call__(self, *children: tuple) -> Self:
        super().__call__(*children)

        self.children.append(
            ChevronsUpDownIcon(
                _class="pointer-events-none shrink-0 text-muted-foreground size-4"
            )
        )

        return self


class SelectValue(Span):
    def __init__(self, **attributes: Unpack[SpanAttributes]):
        base_class_attribute = "pointer-events-none truncate"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            x_text="getDisplayLabel()",
            **{
                ":class": "{ 'text-muted-foreground': isMultiple ? currentLabels.length === 0 : !currentLabels }"
            },
            **attributes,
        )


class SelectValueChips(Span):
    def __init__(
        self,
        variant: Literal["default", "destructive", "outline", "secondary"] = "default",
        **attributes: Unpack[SpanAttributes],
    ):
        base_class_attribute = "pointer-events-none truncate"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            **{
                ":class": "{ 'text-muted-foreground': isMultiple ? currentLabels.length === 0 : !currentLabels }"
            },
            **attributes,
        )

        self.children.extend(
            [
                Template(
                    x_if="isMultiple ? currentLabels.length === 0 : !currentLabels"
                )(Span(x_text="getDisplayLabel()")()),
                Template(
                    x_if="isMultiple ? currentLabels.length !== 0 : currentLabels"
                )(
                    Template(
                        x_for="displayLabel in getDisplayLabel().split(', ').filter(Boolean)",
                    )(Badge(_class="mr-1.5", variant=variant, x_text="displayLabel")())
                ),
            ]
        )


class SelectContent(PopoverContent):
    def __init__(
        self,
        position: Literal["top", "bottom", "left", "right"] = "bottom",
        alignment: Literal["start", "center", "end"] = "start",
        **attributes: Unpack[DivAttributes],
    ):
        base_class_attribute = "p-1"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            position=position,
            alignment=alignment,
            data_popover=True,
            **{
                "@keydown.down.prevent": "focusNext()",
                "@keydown.up.prevent": "focusPrev()",
                "@keydown.enter.prevent": "selectActive()",
            },
            **attributes,
        )


class SelectSearch(Header):
    def __init__(
        self, placeholder: str = "Search...", **attributes: Unpack[InputAttributes]
    ):
        base_class_attribute = "border-b items-center gap-2 flex mb-1 px-3 h-9 -mx-1 -mt-1 [&>svg]:opacity-50 [&>svg]:shrink-0 [&>svg]:size-4"

        forwarded_base_class_attribute = "outline-hidden rounded-md min-w-0 text-sm flex-1 flex bg-transparent py-3 w-full h-10 disabled:opacity-50 disabled:cursor-not-allowed placeholder:text-muted-foreground"
        self.forwarded_class_attribute = attributes.pop("_class", "")
        self.forwarded_attributes = attributes

        super().__init__(_class=base_class_attribute)

        self.children = [
            SearchIcon(),
            Input(
                _class=tw_merge(
                    forwarded_base_class_attribute, self.forwarded_class_attribute
                ),
                type="text",
                placeholder=placeholder,
                autocomplete="off",
                autocorrect="off",
                spellcheck="false",
                role="combobox",
                aria_autocomplete="list",
                x_model="filter",
                x_ref="searchInput",
                **{
                    ":aria-expanded": "isOpen",
                    ":aria-controls": "listboxId",
                    "@input": "activeValue = ''",
                },
                **self.forwarded_attributes,
            ),
        ]

    def __call__(self, *_children: tuple) -> Self:
        warnings.warn(
            f"Trying to add child to a non-child element: {self.__class__.__qualname__}",
            UserWarning,
            stacklevel=2,
        )

        return self


class SelectListbox(Div):
    def __init__(
        self, empty_message: str | None = None, **attributes: Unpack[DivAttributes]
    ):
        base_class_attribute = "outline-hidden [&:not(:has([data-value]:not([aria-hidden=true])))]:before:justify-center [&:not(:has([data-value]:not([aria-hidden=true])))]:before:truncate [&[data-empty]:not(:has([data-value]:not([aria-hidden=true])))]:before:content-[attr(data-empty)] [&:not([data-empty]):not(:has([data-value]:not([aria-hidden=true])))]:before:content-['No_results_found'] [&:not(:has([data-value]:not([aria-hidden=true])))]:before:items-center [&:not(:has([data-value]:not([aria-hidden=true])))]:before:text-sm [&:not(:has([data-value]:not([aria-hidden=true])))]:before:flex [&:not(:has([data-value]:not([aria-hidden=true])))]:before:p-6"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            role="listbox",
            x_ref="listbox",
            data_empty=empty_message,
            tabindex="-1",
            **{
                ":id": "listboxId",
                ":aria-multiselectable": "isMultiple",
                "@mousemove": "activeValue = ''",
            },
            **attributes,
        )


class SelectGroup(Div):
    def __init__(self, **attributes: Unpack[DivAttributes]):
        base_class_attribute = (
            "[&:not(:has([role=option]:not([aria-hidden=true])))]:hidden"
        )
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            role="group",
            **attributes,
        )


class SelectGroupLabel(H3):
    def __init__(self, **attributes: Unpack[HAttributes]):
        base_class_attribute = "text-muted-foreground text-xs flex px-2 py-1.5"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            role="heading",
            **attributes,
        )


class SelectItem(Div):
    def __init__(
        self,
        value: str,
        label: str | None = None,
        disabled: bool = False,
        force: bool = False,
        keywords: list[str] | None = None,
        **attributes: Unpack[DivAttributes],
    ):
        base_class_attribute = "outline-none transition-colors relative rounded-sm cursor-default select-none items-center text-sm flex pl-8 py-1.5 pr-2 w-full group aria-disabled:pointer-events-none aria-disabled:opacity-50 aria-hidden:hidden aria-selected:text-accent-foreground aria-selected:bg-accent/50 hover:text-accent-foreground hover:bg-accent [&.active]:text-accent-foreground [&.active]:bg-accent"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            role="option",
            data_value=value,
            data_slot="select-item",
            data_label=label,
            data_force=force,
            data_keywords=", ".join(keywords) if keywords is not None else None,
            aria_disabled="true" if disabled else "false",
            **{
                "@click": "selectValue($el.dataset.value, $el.dataset.label || $el.textContent.trim())",
                ":aria-selected": r"isMultiple ? currentValue.includes($el.dataset.value) : currentValue === $el.dataset.value",
                ":aria-hidden": "!matchesFilter($el)",
                ":class": "{ 'active': activeValue === $el.dataset.value }",
            },
            **attributes,
        )

    def __call__(self, *children: tuple) -> Self:
        super().__call__(*children)

        self.children.insert(
            0,
            Span(_class="absolute justify-center items-center left-2 flex w-3.5 h-3.5")(
                CheckIcon(
                    _class="transition-opacity duration-200 opacity-0 size-4 group-aria-selected:opacity-100"
                )
            ),
        )
        return self


class SelectSeparator(Hr):
    def __init__(self, **attributes: Unpack[HrAttributes]):
        base_class_attribute = "border-border my-1 -mx-1 [[data-popover]:has(>header_input:not(:placeholder-shown))_&]:hidden"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            role="separator",
            **attributes,
        )
