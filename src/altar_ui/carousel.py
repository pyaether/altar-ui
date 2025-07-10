from collections.abc import Generator, Iterable
from typing import Literal, Self

from aether import BaseWebElement
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
        orientation: Literal["horizontal", "vertical"],
        number_of_slides: int,
        **attributes: Unpack[DivAttributes],
    ):
        base_class_attribute = "relative"
        base_x_data_attribute = AlpineJSData(
            data={
                "carouselOrientation": orientation,
                "slideLength": number_of_slides,
                "currentSlideIndex": 1,
                "previousSlide()": Statement(
                    "{ if (this.currentSlideIndex > 1) { this.currentSlideIndex -= 1 } else { this.currentSlideIndex = this.slideLength } }",
                    seq_type="definition",
                ),
                "nextSlide()": Statement(
                    "{ if (this.currentSlideIndex < this.slideLength) { this.currentSlideIndex += 1 } else { this.currentSlideIndex = 1 } }",
                    seq_type="definition",
                ),
            },
            directive="x-data",
        )
        x_data_attribute = attributes.pop("x_data", None)
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(class_attribute, base_class_attribute),
            x_data=alpine_js_data_merge(base_x_data_attribute, x_data_attribute),
            role="region",
            aria_roledescription="carousel",
            data_slot="carousel",
            **attributes,
        )


class CarouselContent(Div):
    def __init__(self, **attributes: Unpack[DivAttributes]):
        self.forwarded_base_class_attribute = "flex"
        self.forwarded_class_attribute = attributes.pop("_class", "")
        self.forwarded_attributes = attributes

        super().__init__(_class="overflow-hidden", **attributes)

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

        self.children.append(
            Div(
                _class=tw_merge(
                    self.forwarded_class_attribute,
                    self.forwarded_base_class_attribute,
                ),
                **{
                    ":class": "{ '-ml-4': carouselOrientation === 'horizontal', '-mt-4': carouselOrientation !== 'horizontal', 'flex-col': carouselOrientation !== 'horizontal' }"
                },
            )(*forwarded_children)
        )

        return self


class CarouselItem(Div):
    def __init__(self, item_index: int, **attributes: Unpack[DivAttributes]):
        base_class_attribute = "min-w-0 shrink-0 grow-0 basis-full"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(class_attribute, base_class_attribute),
            x_show=f"currentSlideIndex === {item_index + 1}",
            **{
                "x-transition:enter": "animate-in zoom-in-95 fade-in-0",
                "x-transition:leave": "animate-out zoom-out-95 fade-out-0",
                ":class": "{ 'pl-4': carouselOrientation === 'horizontal', 'pt-4': carouselOrientation !== 'horizontal' }",
            },
            role="group",
            aria_roledescription="slide",
            data_slot="carousel-item",
            **attributes,
        )


class CarouselPrevious(Button):
    def __init__(
        self,
        variant: Literal[
            "default", "destructive", "outline", "secondary", "ghost", "link"
        ] = "outline",
        size: Literal["default", "sm", "lg", "icon"] = "icon",
        **attributes: Unpack[PyButtonAttributes],
    ):
        base_class_attribute = "absolute rounded-full size-8"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            variant=variant,
            size=size,
            _class=tw_merge(class_attribute, base_class_attribute),
            **{
                ":class": "{ 'top-1/2': carouselOrientation === 'horizontal', '-left-12': carouselOrientation === 'horizontal', '-translate-y-1/2': carouselOrientation === 'horizontal', '-top-12': carouselOrientation !== 'horizontal', 'left-1/2': carouselOrientation !== 'horizontal', '-translate-x-1/2': carouselOrientation !== 'horizontal', 'rotate-90': carouselOrientation !== 'horizontal' }",
                "@click": "previousSlide()",
                ":disabled": "currentSlideIndex === 1",
            },
            data_slot="carousel-previous",
            **attributes,
        )

        self.children = [
            ArrowLeftIcon(_class="w-4 h-4"),
            Span(_class="sr-only")("Previous Slide"),
        ]


class CarouselNext(Button):
    def __init__(
        self,
        variant: Literal[
            "default", "destructive", "outline", "secondary", "ghost", "link"
        ] = "outline",
        size: Literal["default", "sm", "lg", "icon"] = "icon",
        **attributes: Unpack[PyButtonAttributes],
    ):
        base_class_attribute = "absolute rounded-full size-8"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            variant=variant,
            size=size,
            _class=tw_merge(class_attribute, base_class_attribute),
            **{
                "@click": "nextSlide()",
                ":class": "{ 'top-1/2': carouselOrientation === 'horizontal', '-right-12': carouselOrientation === 'horizontal', '-translate-y-1/2': carouselOrientation === 'horizontal', '-bottom-12': carouselOrientation !== 'horizontal', 'left-1/2': carouselOrientation !== 'horizontal', '-translate-x-1/2': carouselOrientation !== 'horizontal', 'rotate-90': carouselOrientation !== 'horizontal' }",
                ":disabled": "currentSlideIndex === slideLength",
            },
            data_slot="carousel-next",
            **attributes,
        )

        self.children = [
            ArrowRightIcon(_class="w-4 h-4"),
            Span(_class="sr-only")("Next Slide"),
        ]
