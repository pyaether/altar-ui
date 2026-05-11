"""Field

Combine labels, controls, and help text to compose accessible form fields.

Composition:
    Use the following composition to build a Field:

    Fieldset (optional)
    ├── FieldsetLegend (optional)
    ├── FieldDescription (optional)
    └── Field
        ├── FieldLabel
        ├── FieldDescription (optional)
        ├── FieldSection (groups FieldLabel + FieldDescription together)
        │   ├── FieldLabel (used inside FieldSection for horizontal layouts)
        │   └── FieldDescription
        ├── ... input / select / textarea / etc.
        └── FieldAlert (optional)
"""

from enum import StrEnum
from typing import Literal

from aether.plugins.alpinejs import AlpineJSData, Statement, alpine_js_data_merge
from aether.plugins.tailwindcss import tw_merge
from aether.tags.html import (
    Div,
    DivAttributes,
    FieldsetAttributes,
    LabelAttributes,
    Legend,
    LegendAttributes,
    P,
    PAttributes,
    Section,
    SectionAttributes,
)
from aether.tags.html import Fieldset as PyFieldset

from .label import Label

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack  # noqa: UP035


class Fieldset(PyFieldset):
    def __init__(self, **attributes: Unpack[FieldsetAttributes]):
        base_class_attribute = "flex-col gap-6 flex"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute), **attributes
        )


class FieldsetLegend(Legend):
    def __init__(self, **attributes: Unpack[LegendAttributes]):
        base_class_attribute = "font-medium text-base mb-3"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute), **attributes
        )


class FieldsetDescription(P):
    def __init__(self, **attributes: Unpack[PAttributes]):
        base_class_attribute = "leading-normal font-normal text-muted-foreground text-sm -mt-1.5 [&>a:hover]:text-primary [&>a]:underline [&>a]:underline-offset-4"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute), **attributes
        )


class FieldOrientation(StrEnum):
    vertical = "flex-col [&>*]:w-full"
    horizontal = "flex-row items-center [&>label]:flex-auto [&_p]:text-balance has-[section]:items-start has-[section]:[&_input[type=checkbox]]:mt-px has-[section]:[&_input[type=radio]]:mt-px"
    none = "[&>*]:w-full"


class Field(Div):
    def __init__(
        self,
        orientation: Literal["vertical", "horizontal"] | None = "vertical",
        invalid: bool | None = False,
        disabled: bool = False,
        **attributes: Unpack[DivAttributes],
    ):
        base_x_data_attribute = AlpineJSData(
            data={
                "fieldId": Statement("$id('field')", seq_type="assignment"),
                "descriptionId": Statement(
                    "$id('field') + '-desc'", seq_type="assignment"
                ),
                "alertId": Statement("$id('field') + '-alert'", seq_type="assignment"),
            },
            directive="x-data",
        )
        base_class_attribute = "gap-3 flex w-full group data-[invalid=true]:text-destructive [&>.sr-only]:w-auto"
        orientation_class_attribute = (
            FieldOrientation[orientation]
            if orientation is not None
            else FieldOrientation["none"]
        )

        class_attribute = attributes.pop("_class", "")
        x_data_attribute = attributes.pop("x_data", None)

        x_id_attribute = attributes.pop("x_id", "['field']")

        super().__init__(
            _class=tw_merge(
                orientation_class_attribute, base_class_attribute, class_attribute
            ),
            x_data=alpine_js_data_merge(base_x_data_attribute, x_data_attribute),
            x_id=x_id_attribute,
            role="group",
            data_invalid="true" if invalid else "false",
            data_disabled="true" if disabled else "false",
        )


class FieldLabel(Label):
    def __init__(self, **attributes: Unpack[LabelAttributes]):
        base_class_attribute = "transition-colors leading-snug items-center font-medium text-sm gap-2 flex w-fit group-data-[disabled=true]:pointer-events-none group-data-[disabled=true]:opacity-50"
        class_attribute = attributes.pop("_class", "")

        if not attributes.get("_for") and not attributes.get(":for"):
            attributes[":for"] = "fieldId"

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute), **attributes
        )


class FieldSection(Section):
    def __init__(self, **attributes: Unpack[SectionAttributes]):
        base_class_attribute = "flex-col leading-snug flex-1 gap-1.5 flex"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute), **attributes
        )


class FieldDescription(P):
    def __init__(self, **attributes: Unpack[PAttributes]):
        base_class_attribute = "leading-normal font-normal text-muted-foreground text-sm last:mt-0 [&>a:hover]:text-primary [&:nth-last-child(2)]:-mt-1 [&>a]:underline [&>a]:underline-offset-4"
        class_attribute = attributes.pop("_class", "")

        if not attributes.get("id") and not attributes.get(":id"):
            attributes[":id"] = "descriptionId"

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute), **attributes
        )


class FieldAlert(Div):
    def __init__(self, **attributes: Unpack[DivAttributes]):
        base_class_attribute = "font-normal text-sm text-destructive [&_ul]:flex-col [&_ul]:list-disc [&_ul]:gap-1 [&_ul]:flex [&_ul]:ml-4"
        class_attribute = attributes.pop("_class", "")

        if not attributes.get("id") and not attributes.get(":id"):
            attributes[":id"] = "alertId"

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            role="alert",
            aria_live="polite",
            **attributes,
        )
