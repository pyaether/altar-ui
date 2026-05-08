"""Carousel

A carousel with motion and swipe.

Composition:
    Use the following composition to build a Carousel:

    Carousel
    ├── CarouselPrevious
    ├── CarouselContent
    │   ├── CarouselItem
    │   └── CarouselItem
    └── CarouselNext
"""

from typing import Literal

from aether.plugins.alpinejs import AlpineJSData, Statement, alpine_js_data_merge
from aether.plugins.tailwindcss import tw_merge
from aether.tags.html import ButtonAttributes as PyButtonAttributes
from aether.tags.html import Div, DivAttributes, Span
from altar_icons import ArrowLeftIcon, ArrowRightIcon

from .button import Button

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack  # noqa: UP035


class Carousel(Div):
    def __init__(
        self,
        number_of_slides: int,
        orientation: Literal["horizontal", "vertical"] = "horizontal",
        **attributes: Unpack[DivAttributes],
    ):
        base_class_attribute = (
            "flex items-center gap-2"
            if orientation == "horizontal"
            else "flex flex-col items-center gap-2"
        )
        base_x_data_attribute = AlpineJSData(
            data={
                "carouselOrientation": orientation,
                "slideLength": number_of_slides,
                "currentSlideIndex": 1,
                "previousSlide()": Statement(
                    "{ this.currentSlideIndex > 1 ? this.currentSlideIndex -= 1 : this.currentSlideIndex = this.slideLength; $refs.track.children[this.currentSlideIndex - 1].scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'nearest' }) }",
                    seq_type="definition",
                ),
                "nextSlide()": Statement(
                    "{ this.currentSlideIndex < this.slideLength ? this.currentSlideIndex += 1 : this.currentSlideIndex = 1; $refs.track.children[this.currentSlideIndex - 1].scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'nearest' }) }",
                    seq_type="definition",
                ),
            },
            directive="x-data",
        )
        x_data_attribute = attributes.pop("x_data", None)
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            x_data=alpine_js_data_merge(base_x_data_attribute, x_data_attribute),
            role="region",
            aria_roledescription="carousel",
            **attributes,
        )


class CarouselContent(Div):
    def __init__(self, **attributes: Unpack[DivAttributes]):
        base_class_attribute = "overflow-hidden scroll-smooth snap-mandatory flex [&::-webkit-scrollbar]:hidden [scrollbar-width:none]"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            x_ref="track",
            **{
                ":class": "{ 'snap-x': carouselOrientation === 'horizontal', 'overflow-x-auto': carouselOrientation === 'horizontal', 'snap-y': carouselOrientation === 'vertical', 'overflow-y-auto': carouselOrientation === 'vertical', 'flex-col': carouselOrientation === 'vertical' }",
                "@scrollend": "currentSlideIndex = carouselOrientation === 'horizontal' ? Math.round($el.scrollLeft / $el.clientWidth) + 1 : Math.round($el.scrollTop / $el.clientHeight) + 1",
            },
            **attributes,
        )


class CarouselItem(Div):
    def __init__(self, **attributes: Unpack[DivAttributes]):
        base_class_attribute = "basis-full shrink-0 min-w-0 snap-start grow-0"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            **{
                ":class": "{ 'px-4': carouselOrientation === 'horizontal', 'py-4': carouselOrientation === 'vertical'}",
            },
            role="group",
            aria_roledescription="slide",
            **attributes,
        )


class CarouselPrevious(Button):
    def __init__(
        self,
        variant: Literal[
            "default", "destructive", "outline", "secondary", "ghost", "link"
        ] = "outline",
        size: Literal["default", "sm", "lg", "icon", "icon_sm", "icon_lg"] = "icon",
        **attributes: Unpack[PyButtonAttributes],
    ):
        base_class_attribute = "rounded-full shrink-0 size-8"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            variant=variant,
            size=size,
            _class=tw_merge(base_class_attribute, class_attribute),
            **{
                "@click": "previousSlide()",
                ":class": "{ 'rotate-90': carouselOrientation === 'vertical' }",
                ":disabled": "currentSlideIndex === 1",
            },
            **attributes,
        )

        self.children = [
            ArrowLeftIcon(_class="size-4"),
            Span(_class="sr-only")("Previous Slide"),
        ]


class CarouselNext(Button):
    def __init__(
        self,
        variant: Literal[
            "default", "destructive", "outline", "secondary", "ghost", "link"
        ] = "outline",
        size: Literal["default", "sm", "lg", "icon", "icon_sm", "icon_lg"] = "icon",
        **attributes: Unpack[PyButtonAttributes],
    ):
        base_class_attribute = "rounded-full shrink-0 size-8"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            variant=variant,
            size=size,
            _class=tw_merge(base_class_attribute, class_attribute),
            **{
                "@click": "nextSlide()",
                ":class": "{ 'rotate-90': carouselOrientation === 'vertical' }",
                ":disabled": "currentSlideIndex === slideLength",
            },
            **attributes,
        )

        self.children = [
            ArrowRightIcon(_class="size-4"),
            Span(_class="sr-only")("Next Slide"),
        ]
