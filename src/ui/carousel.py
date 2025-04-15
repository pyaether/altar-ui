from collections.abc import Generator, Iterable
from typing import Literal, Self

from pytempl import BaseWebElement
from pytempl.plugins.tailwindcss import tw_merge
from pytempl.tags.html import (
    ButtonAttributes as PyButtonAttributes,
)
from pytempl.tags.html import (
    Div,
    DivAttributes,
    Span,
)
from pytempl_icons import ArrowLeftIcon, ArrowRightIcon

from .button import Button

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class Carousel(Div):
    def __init__(
        self,
        orientation: Literal["horizontal", "vertical"],
        number_of_slides: int,
        **attributes: Unpack[DivAttributes],
    ):
        base_class_attribute = "relative"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(class_attribute, base_class_attribute),
            role="region",
            aria_roledescription="carousel",
            x_data=f'{{ carouselOrientation: "{orientation}", slideLength: {number_of_slides}, currentSlideIndex: 1, previousSlide() {{if (this.currentSlideIndex > 1) {{this.currentSlideIndex = this.currentSlideIndex - 1}} else {{this.currentSlideIndex = this.slideLength}} }}, nextSlide() {{if (this.currentSlideIndex < this.slideLength) {{this.currentSlideIndex = this.currentSlideIndex + 1}} else {{this.currentSlideIndex = 1}} }} }}',
            **attributes,
        )


class CarouselContent(Div):
    def __init__(self, **attributes: Unpack[DivAttributes]):
        self.forwarded_base_class_attribute = "flex"
        self.forwarded_class_attribute = attributes.pop("_class", "")
        self.forwarded_attributes = attributes

        super().__init__(
            _class="overflow-hidden",
            **attributes,
        )

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
                    ":class": "carouselOrientation === 'horizontal' ? '-ml-4' : '-mt-4 flex-col'"
                },
            )(*forwarded_children)
        )

        return self


class CarouselItem(Div):
    def __init__(self, item_index: int, **attributes: Unpack[DivAttributes]):
        base_class_attribute = "min-w-0 shrink-0 grow-0 basis-full"
        class_attribute = attributes.pop("_class", "")
        slide_index = item_index + 1

        super().__init__(
            _class=tw_merge(class_attribute, base_class_attribute),
            x_show=f"currentSlideIndex === {slide_index}",
            **{":class": "carouselOrientation === 'horizontal' ? 'pl-4' : 'pt-4'"},
            role="group",
            aria_roledescription="slide",
            **attributes,
        )


class CarouselPrevious(Button):
    def __init__(self, **attributes: Unpack[PyButtonAttributes]):
        base_class_attribute = "absolute h-8 w-8 rounded-full"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            variant="outline",
            size="icon",
            _class=tw_merge(class_attribute, base_class_attribute),
            **{
                ":class": "carouselOrientation === 'horizontal' ? '-left-12 top-1/2 -translate-y-1/2' : '-top-12 left-1/2 -translate-x-1/2 rotate-90'",
                "@click": "previousSlide()",
                ":disabled": "currentSlideIndex === 1",
            },
            aria_label="previous slide",
            **attributes,
        )

        self.children = [
            ArrowLeftIcon(_class="h-4 w-4"),
            Span(_class="sr-only")("Previous Slide"),
        ]


class CarouselNext(Button):
    def __init__(self, **attributes: Unpack[PyButtonAttributes]):
        base_class_attribute = "absolute h-8 w-8 rounded-full"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            variant="outline",
            size="icon",
            _class=tw_merge(class_attribute, base_class_attribute),
            **{
                ":class": "carouselOrientation === 'horizontal' ? '-right-12 top-1/2 -translate-y-1/2' : '-bottom-12 left-1/2 -translate-x-1/2 rotate-90'",
                "@click": "nextSlide()",
                ":disabled": "currentSlideIndex === slideLength",
            },
            aria_label="next slide",
            **attributes,
        )

        self.children = [
            ArrowRightIcon(_class="h-4 w-4"),
            Span(_class="sr-only")("Next Slide"),
        ]
