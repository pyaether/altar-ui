"""Toast

A succinct message that is displayed temporarily.

Composition:
    Use the following composition to build a Toast:

    Toaster
    ├── Toast (SSR / HTMX / Hardcoded)
    │   ├── ToastContent
    │   │   ├── ToastSection
    │   │   │   ├── ToastTitle
    │   │   │   └── ToastDescription
    │   │   └── ToastFooter
    │   │       └── ToastAction
    └── Template (Dynamic frontend via @altar:toast event)
"""

from enum import Enum, StrEnum
from typing import Literal, Self

from aether.plugins.alpinejs import AlpineJSData, Statement, alpine_js_data_merge
from aether.plugins.tailwindcss import tw_merge
from aether.tags.html import (
    H2,
    Div,
    DivAttributes,
    Footer,
    FooterAttributes,
    HAttributes,
    P,
    PAttributes,
    Section,
    SectionAttributes,
    Template,
)
from aether.tags.html import ButtonAttributes as PyButtonAttributes
from altar_icons import (
    CircleAlertIcon,
    CircleCheckIcon,
    CircleXIcon,
    ExclamationTriangleIcon,
)

from .button import Button

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack  # noqa: UP035


class ToasterAlign(StrEnum):
    start = "left-0"
    center = "left-1/2 -translate-x-1/2"
    end = "right-0"


class ToasterPosition(StrEnum):
    bottom = "bottom-0"
    top = "top-0"


class ToastCategoryIcon(Enum):
    success = CircleCheckIcon()
    info = CircleAlertIcon()
    warning = ExclamationTriangleIcon()
    error = CircleXIcon()


class Toaster(Div):
    def __init__(
        self,
        position: Literal["top", "bottom"] = "bottom",
        align: Literal["start", "center", "end"] = "end",
        **attributes: Unpack[DivAttributes],
    ):
        base_class_attribute = "pointer-events-none flex-col-reverse fixed flex w-full z-50 p-4 sm:max-w-90"
        align_class_attribute = ToasterAlign[align]
        position_class_attribute = ToasterPosition[position]
        class_attribute = attributes.pop("_class", "")

        base_x_data_attribute = AlpineJSData(
            data={
                "isPaused": False,
                "dynamicToasts": [],
                "addToast(event)": Statement(
                    r"""{
                        const config = event.detail || {};
                        const isError = config.category === 'error';

                        this.dynamicToasts.push({
                            id: Date.now() + Math.random(),
                            category: config.category || 'info',
                            title: config.title || '',
                            description: config.description || '',
                            actions: config.actions || [],
                            duration: config.duration !== undefined ? config.duration : (isError ? 5000 : 3000)
                        });
                    }""",
                    seq_type="definition",
                ),
                "removeDynamicToast(id)": Statement(
                    "{ this.dynamicToasts = this.dynamicToasts.filter(toast => toast.id !== id); }",
                    seq_type="definition",
                ),
            },
            directive="x-data",
        )
        x_data_attribute = attributes.pop("x_data", None)

        super().__init__(
            id="toaster",
            _class=tw_merge(
                align_class_attribute,
                position_class_attribute,
                base_class_attribute,
                class_attribute,
            ),
            aria_live="polite",
            aria_label="Notifications",
            x_data=alpine_js_data_merge(base_x_data_attribute, x_data_attribute),
            **{
                "@mouseenter": "isPaused = true",
                "@mouseleave": "isPaused = false",
                "@altar:toast.window": "addToast($event)",
            },
            **attributes,
        )

    def __call__(self, *children: tuple) -> Self:
        super().__call__(*children)

        self.children.append(
            Template(x_for="toast in dynamicToasts", **{":key": "toast.id"})(
                Toast(
                    category=None,
                    **{
                        ":data-duration": "toast.duration",
                        ":data-category": "toast.category",
                    },
                )(
                    ToastContent(category=None)(
                        Template(x_if="toast.category === 'success'")(
                            CircleCheckIcon()
                        ),
                        Template(x_if="toast.category === 'info'")(CircleAlertIcon()),
                        Template(x_if="toast.category === 'warning'")(
                            ExclamationTriangleIcon()
                        ),
                        Template(x_if="toast.category === 'error'")(CircleXIcon()),
                        ToastSection()(
                            ToastTitle(x_show="toast.title", x_text="toast.title")(),
                            ToastDescription(
                                x_show="toast.description", x_text="toast.description"
                            )(),
                        ),
                        ToastFooter(x_show="toast.actions")(
                            Template(
                                x_for="action in toast.actions",
                                **{":key": "action.label"},
                            )(
                                ToastAction(
                                    x_text="action.label || 'Action'",
                                    **{
                                        "@click": "if (action.onclick) action.onclick()"
                                    },
                                )()
                            )
                        ),
                    )
                )
            )
        )

        return self


class Toast(Div):
    def __init__(
        self,
        category: Literal["success", "info", "warning", "error"] | None = "info",
        duration: int | None = None,
        **attributes: Unpack[DivAttributes],
    ):
        base_class_attribute = (
            "pointer-events-auto w-full mt-4 animate-[toast-up_0.3s_ease-in-out] grid grid-rows-[1fr] transition-[grid-template-rows,opacity,margin] duration-300 ease-in-out "
            "aria-hidden:grid-rows-[0fr] aria-hidden:opacity-0 aria-hidden:m-0 aria-hidden:border-0 aria-hidden:p-0 aria-hidden:overflow-hidden"
        )
        class_attribute = attributes.pop("_class", "")

        toast_x_data = AlpineJSData(
            data={
                "isOpen": True,
                "remainingTime": 0,
                "startTime": None,
                "timeoutId": None,
                "init()": Statement(
                    r"""{
                        const duration = parseInt(this.$el.dataset.duration);
                        this.remainingTime = isNaN(duration) ? (this.$el.dataset.category === 'error' ? 5000 : 3000) : duration;
                    }""",
                    seq_type="definition",
                ),
                "start()": Statement(
                    r"""{
                        if (this.remainingTime === -1 || this.timeoutId) return;

                        this.startTime = Date.now();
                        this.timeoutId = setTimeout(() => this.close(), this.remainingTime);
                    }""",
                    seq_type="definition",
                ),
                "pause()": Statement(
                    r"""{
                        if (!this.timeoutId) return;

                        clearTimeout(this.timeoutId);
                        this.timeoutId = null;

                        this.remainingTime -= (Date.now() - this.startTime);
                    }""",
                    seq_type="definition",
                ),
                "close()": Statement(
                    r"""{
                        clearTimeout(this.timeoutId); this.timeoutId = null;

                        if (this.$el.contains(document.activeElement)) document.activeElement.blur();

                        this.isOpen = false;
                    }""",
                    seq_type="definition",
                ),
            },
            directive="x-data",
        )

        x_data_attribute = attributes.pop("x_data", None)

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            x_data=alpine_js_data_merge(toast_x_data, x_data_attribute),
            x_effect="isPaused ? pause() : start()",
            **{
                ":aria-hidden": "!isOpen",
                "@transitionend.self": r"""if (!isOpen) { typeof toast !== 'undefined' && toast.id ? removeDynamicToast(toast.id) : $el.remove(); }""",
            },
            data_category=category,
            data_duration=str(duration) if duration is not None else None,
            **attributes,
        )


class ToastContent(Div):
    def __init__(
        self,
        category: Literal["success", "info", "warning", "error"] | None = "info",
        **attributes: Unpack[DivAttributes],
    ):
        base_class_attribute = "overflow-hidden rounded-lg shadow-lg border items-center text-popover-foreground text-[13px] gap-2.5 flex bg-popover p-3 [[aria-hidden=true]_&]:border-0 [&_svg]:shrink-0 [&_svg:not([class*='size-'])]:size-4"

        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            role="alert" if category == "error" else "status",
            aria_atomic="true",
            aria_live="assertive" if category == "error" else "polite",
            **attributes,
        )

        if category is not None:
            toast_category_icon = ToastCategoryIcon[category]
            self.children.append(toast_category_icon)


class ToastSection(Section):
    def __init__(self, **attributes: Unpack[SectionAttributes]):
        super().__init__(**attributes)


class ToastTitle(H2):
    def __init__(self, **attributes: Unpack[HAttributes]):
        base_class_attribute = "tracking-tight font-medium"
        class_attribute = attributes.pop("_class", "")
        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute), **attributes
        )


class ToastDescription(P):
    def __init__(self, **attributes: Unpack[PAttributes]):
        base_class_attribute = "break-all text-muted-foreground"
        class_attribute = attributes.pop("_class", "")
        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute), **attributes
        )


class ToastFooter(Footer):
    def __init__(self, **attributes: Unpack[FooterAttributes]):
        base_class_attribute = "flex-col gap-2 flex ml-auto"
        class_attribute = attributes.pop("_class", "")
        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute), **attributes
        )


class ToastAction(Button):
    def __init__(
        self,
        variant: Literal[
            "default", "destructive", "outline", "secondary", "ghost", "link"
        ] = "outline",
        size: Literal["default", "sm", "lg", "icon", "icon_sm", "icon_lg"] = "sm",
        **attributes: Unpack[PyButtonAttributes],
    ):
        base_class_attribute = "text-xs px-2.5 h-6"
        base_click_event_attribute = "close()"
        click_event_attribute = attributes.pop("@click", "").strip(" ;").strip(";")
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            type="button",
            variant=variant,
            size=size,
            _class=tw_merge(base_class_attribute, class_attribute),
            **{
                "@click": f"{click_event_attribute}; {base_click_event_attribute}".strip(
                    "; "
                )
            },
            **attributes,
        )
