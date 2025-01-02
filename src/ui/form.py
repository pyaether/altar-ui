from typing import Any, Dict, Mapping, Sequence

from pytempl.plugins.tailwindcss import tw_merge
from pytempl.tags.html import (
    Div,
    DivAttributes,
    P,
    PAttributes,
)
from pytempl.tags.html import Form as PyForm
from pytempl.tags.html import FormAttributes as PyFormAttributes
from pytempl.tags.html import (
    LabelAttributes as PyLabelAttributes,
)

from .label import Label

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


def convert_dict_to_x_data(data: Dict[str, Any]) -> str:
    data_list = []
    for key, value in data.items():
        if isinstance(value, str):
            data_list.append(f"{key}: '{value}'")
        elif isinstance(value, bool):
            data_list.append(f"{key}: {str(value).lower()}")
        elif isinstance(value, (int, float, Sequence)):
            data_list.append(f"{key}: {value}")
        elif isinstance(value, Mapping):
            data_list.append(f"{key}: {convert_dict_to_x_data(value)}")
        else:
            raise ValueError(f"Unsupported value type: {type(value)}")

    return f"{{{', '.join(data_list)}}}"


def convert_dict_to_x_init(data: Dict[str, Any]) -> str:
    data_list = []
    for key, value in data.items():
        if isinstance(value, str):
            data_list.append(f"{key} = '{value}'")
        elif isinstance(value, bool):
            data_list.append(f"{key} = {str(value).lower()}")
        elif isinstance(value, (int, float, Sequence)):
            data_list.append(f"{key} = {value}")
        elif isinstance(value, Mapping):
            data_list.append(f"{key} = {convert_dict_to_x_data(value)}")
        else:
            raise ValueError(f"Unsupported value type: {type(value)}")

    return f"{', '.join(data_list)}"


class Form(PyForm):
    def __init__(
        self,
        x_form_data_struct: Dict[str, Any] = None,
        **attributes: Unpack[PyFormAttributes],
    ):
        if x_form_data_struct:
            super().__init__(
                x_data=convert_dict_to_x_data(x_form_data_struct),
                **attributes,
            )
        else:
            super().__init__(**attributes)


class FormField(Div):
    def __init__(
        self,
        x_form_field_init_data: Dict[str, Any] = None,
        **attributes: Unpack[DivAttributes],
    ):
        if x_form_field_init_data:
            super().__init__(
                x_init=convert_dict_to_x_init(x_form_field_init_data), **attributes
            )
        else:
            super().__init__(**attributes)


class FormItem(Div):
    def __init__(self, **attributes: Unpack[DivAttributes]):
        base_class_attribute = "space-y-2"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(class_attribute, base_class_attribute),
            x_data="{ formItemId: $id('form-item'), formDescriptionId: $id('form-item-description'), formMessageId: $id('form-item-message'), error: '' }",
            **attributes,
        )


class FormLabel(Label):
    def __init__(self, **attributes: Unpack[PyLabelAttributes]):
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=class_attribute,
            **{":class": "error && 'text-destructive'", ":for": "`${formItemId}`"},
            **attributes,
        )


class FormControl(Div):
    def __init__(self, **attributes: Unpack[DivAttributes]) -> None:
        super().__init__(
            **{
                ":id": "`${formItemId}`",
                ":aria-describedby": "!error ? `${formDescriptionId}` : `${formDescriptionId} ${formMessageId}`",
                ":aria-invalid": "!!error",
            },
            **attributes,
        )


class FormDescription(P):
    def __init__(self, **attributes: Unpack[PAttributes]):
        base_class_attribute = "text-[0.8rem] text-muted-foreground"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(class_attribute, base_class_attribute),
            **{":id": "`${formDescriptionId}`"},
            **attributes,
        )


# TODO: Add logic to display error messages based on the 'error' attribute of the FormItem component.
# ref doc: https://github.com/shadcn-ui/ui/blob/main/apps/www/registry/new-york/ui/form.tsx#L145-L167
class FormMessage(P):
    def __init__(self, is_errored: bool = False, **attributes: Unpack[PAttributes]):
        base_class_attribute = "text-[0.8rem] font-medium text-destructive"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(class_attribute, base_class_attribute),
            x_init=f"error = {str(is_errored).lower()}",
            x_show="error",
            **{":id": "`${formMessageId}`"},
            **attributes,
        )
