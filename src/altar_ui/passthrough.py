from collections.abc import Generator
from typing import Self

from aether import BaseWebElement
from aether.base import _render_element
from aether.errors import ValidationError
from aether.tags.html import BaseHTMLElement, GlobalHTMLAttributes
from aether.utils import (
    ValidatorFunction,
    format_validation_error_message,
    validate_dictionary_data,
)
from pydantic import ValidationError as PydanticValidationError

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack  # noqa: UP035


class PassthroughAttributes(GlobalHTMLAttributes):
    @classmethod
    def validate(
        cls,
        data: dict,
        default_values: dict | None = None,
        custom_validators: list[ValidatorFunction] | None = None,
    ) -> Self:
        return validate_dictionary_data(cls, data, default_values, custom_validators)


class Passthrough(BaseHTMLElement):
    tag_name = "passthrough"
    have_children = True
    content_category = None

    def __init__(self, **attributes: Unpack[PassthroughAttributes]):
        try:
            validated_attributes = PassthroughAttributes.validate(attributes)
        except (ValidationError, PydanticValidationError) as err:
            raise ValueError(format_validation_error_message(err))

        super().__init__(**validated_attributes)

    def __call__(self, *children: tuple):
        allowed_child_types = (BaseWebElement,)

        if len(children) != 1:
            raise ValueError(
                f"`{self.__class__.__qualname__}` must be called with exactly one child, but got {len(children)}."
            )
        else:
            child = children[0]
            if isinstance(child, allowed_child_types):
                # TODO: Improve merging logic

                current_attributes = child.attributes
                passthrough_attributes = self.attributes
                combined_attributes = passthrough_attributes | current_attributes

                child.attributes = combined_attributes
                child.attributes["class"] = current_attributes.pop(
                    "class", None
                ) or passthrough_attributes.pop("class", None)

                self.children.append(child)
            else:
                raise ValueError(
                    f"Invalid child type found. `{self.__class__.__qualname__}` can only have {', '.join([type(allowed_type).__class__.__qualname__ for allowed_type in allowed_child_types])}."
                )

        return self

    def render(self, stringify: bool = True) -> Generator[str]:
        for child in self.children:
            yield from _render_element(child, stringify, self.escape_quote)
