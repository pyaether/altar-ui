import warnings
from typing import Any, Self

from aether.plugins.alpinejs import (
    AlpineHookForm,
    AlpineJSData,
    Statement,
    alpine_js_data_merge,
)
from aether.plugins.tailwindcss import tw_merge
from aether.tags.html import (
    Div,
    DivAttributes,
    P,
    PAttributes,
)
from aether.tags.html import Form as PyForm
from aether.tags.html import FormAttributes as PyFormAttributes
from aether.tags.html import Input as PyInput
from aether.tags.html import (
    LabelAttributes as PyLabelAttributes,
)
from aether.tags.html import Textarea as PyTextarea

from .checkbox import Checkbox
from .input import PasswordInput
from .label import Label
from .radio import RadioGroupItem
from .switch import Switch

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class Form(PyForm):
    def __init__(self, **attributes: Unpack[PyFormAttributes]):
        base_x_data_attribute = AlpineJSData(
            data={"form_fields": []}, directive="x-data"
        )
        x_data_attribute = attributes.pop("x_data", None)

        super().__init__(
            x_data=alpine_js_data_merge(base_x_data_attribute, x_data_attribute),
            data_slot="form",
            **attributes,
        )


class FormField(Div):
    def __init__(self, **attributes: Unpack[DivAttributes]):
        base_x_data_attribute = AlpineJSData(
            data={
                "field_id": Statement(
                    content="$id('form-field-id')", seq_type="assignment"
                ),
                "has_error": None,
                "updateHasErrorValueInParent(id, value)": Statement(
                    """{
                        const field_item = form_fields.find(field => field.id === id);
                        if (field_item) {
                            field_item.has_error = value;
                        }
                    }""",
                    seq_type="definition",
                ),
            },
            directive="x-data",
        )
        base_x_effect_attribute = AlpineJSData(
            data={
                "update_has_error_value_for_form_field": Statement(
                    "updateHasErrorValueInParent(field_id, has_error)",
                    seq_type="instance",
                )
            },
            directive="x-effect",
        )
        base_x_init_attribute = AlpineJSData(
            data={
                "append_to_form_fields_array": Statement(
                    "form_fields.push({ id: field_id, has_error: has_error })",
                    seq_type="instance",
                )
            },
            directive="x-init",
        )
        x_data_attribute = attributes.pop("x_data", None)
        x_effect_attribute = attributes.pop("x_effect", None)
        x_init_attribute = attributes.pop("x_init", None)

        super().__init__(
            x_data=alpine_js_data_merge(base_x_data_attribute, x_data_attribute),
            x_effect=alpine_js_data_merge(base_x_effect_attribute, x_effect_attribute),
            x_init=alpine_js_data_merge(base_x_init_attribute, x_init_attribute),
            data_slot="form-field",
            **attributes,
        )


class FormItem(Div):
    def __init__(self, **attributes: Unpack[DivAttributes]):
        base_class_attribute = "grid gap-2"
        base_x_data_attribute = AlpineJSData(
            data={
                "has_error": None,
                "error_message": "",
                "form_fields": [],
                "updateHasErrorValueInParent(value)": Statement(
                    "{ has_error = value; }",
                    seq_type="definition",
                ),
                "updateErrorMessageValueInParent(value)": Statement(
                    "{ error_message = value; }",
                    seq_type="definition",
                ),
            },
            directive="x-data",
        )
        base_x_init_attribute = AlpineJSData(
            data={
                "update_has_error_value_for_form_field": Statement(
                    """
                    Alpine.effect(() => {
                        if (form_fields.length > 0) {
                            const form_fields_has_error = form_fields.some(field => field["has_error"] === true);
                            if (form_fields_has_error) {
                                has_error = form_fields_has_error;
                                error_message = "Invalid Value";
                            } else {
                                has_error = false;
                                error_message = null;
                            }
                        }
                    })

                    Alpine.effect(() => {
                        updateHasErrorValueInParent(has_error);
                        updateErrorMessageValueInParent(error_message);
                    })
                    """,
                    seq_type="instance",
                )
            },
            directive="x-init",
        )
        class_attribute = attributes.pop("_class", "")
        x_data_attribute = attributes.pop("x_data", None)
        x_init_attribute = attributes.pop("x_init", None)

        super().__init__(
            _class=tw_merge(class_attribute, base_class_attribute),
            x_data=alpine_js_data_merge(base_x_data_attribute, x_data_attribute),
            x_init=alpine_js_data_merge(base_x_init_attribute, x_init_attribute),
            x_id="['form-description', 'form-item-id', 'form-message']",
            data_slot="form-item",
            **attributes,
        )


class FormLabel(Label):
    def __init__(self, **attributes: Unpack[PyLabelAttributes]):
        data_error_class_attribute = "data-[error=true]:text-destructive"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(class_attribute, data_error_class_attribute),
            data_slot="form-label",
            **{
                ":data-error": "has_error",
                ":for": Statement(content="$id('form-item-id')", seq_type="assignment"),
            },
            **attributes,
        )


class FormControl(Div):
    def __init__(
        self, hook_form_item: AlpineHookForm | None, **attributes: Unpack[DivAttributes]
    ):
        self.hook_form_item = hook_form_item
        base_x_data_attribute = AlpineJSData(
            data={
                "runValidation(value, conditional, max_length, min_length)": Statement(
                    f"""{{
                        if (conditional instanceof RegExp){{
                            if (conditional.test(value) === false) {{
                                has_error = true;
                                if (min_length && value.length > 0 && value.length < min_length ) {{
                                    error_message = `Must be at least ${{min_length}} characters.`;
                                }} else if (max_length && value.length > max_length) {{
                                    error_message = `Must be at most ${{max_length}} characters.`;
                                }} else {{
                                    error_message = "{self.hook_form_item.validator.get("validation_fail_message", "Enter valid value.") if self.hook_form_item is not None else "Enter valid value."}";
                                }}
                            }} else {{
                                has_error = false;
                                error_message = null;
                            }}
                        }} else if (conditional instanceof Function) {{
                            const validation_failed = conditional(value)
                            if (validation_failed) {{
                                has_error = true;
                                error_message = "{self.hook_form_item.validator.get("validation_fail_message", "Enter valid value.") if self.hook_form_item is not None else "Enter valid value."}";
                            }} else {{
                                has_error = false;
                                error_message = null;
                            }}
                        }} else {{
                            has_error = false;
                            error_message = null;
                        }}
                    }}""",
                    seq_type="definition",
                ),
                "getHasError()": Statement(
                    "{ if (has_error === null) { return false } else { return has_error } }",
                    seq_type="definition",
                ),
            },
            directive="x-data",
        )
        class_attribute = attributes.pop("_class", "")
        x_data_attribute = attributes.pop("x_data", None)

        super().__init__(
            _class=class_attribute,
            data_slot="form-control",
            x_data=alpine_js_data_merge(base_x_data_attribute, x_data_attribute),
            **attributes,
        )

    def __call__(self, *children: Any) -> Self:
        allowed_child_types = (
            Checkbox,
            PasswordInput,
            PyInput,
            PyTextarea,
            RadioGroupItem,
            Switch,
        )

        if self.have_children:
            if len(children) != 1:
                raise ValueError(
                    f"`{self.__class__.__qualname__}` must be called with exactly one child, but got {len(children)}."
                )
            else:
                child = children[0]
                if isinstance(child, allowed_child_types):
                    current_attributes = {}
                    update_attributes = {}

                    if isinstance(
                        child, Checkbox | PasswordInput | RadioGroupItem | Switch
                    ):
                        if forwarded_attributes := getattr(
                            child, "forwarded_attributes", None
                        ):
                            current_attributes.update(forwarded_attributes)
                        if forwarded_class_attribute := getattr(
                            child, "forwarded_class_attribute", None
                        ):
                            current_attributes["_class"] = forwarded_class_attribute
                    else:
                        current_attributes = child.attributes

                    update_attributes[":id"] = Statement(
                        content="$id('form-item-id')", seq_type="assignment"
                    )
                    update_attributes[":aria-describedby"] = (
                        "getHasError() ? $id('form-description') : `${$id('form-description')} ${$id('form-message')}`"
                    )
                    update_attributes[":aria-invalid"] = "getHasError()"

                    if self.hook_form_item is not None:
                        if self.hook_form_item.name is not None:
                            update_attributes["name"] = self.hook_form_item.name

                        if self.hook_form_item.required is not None:
                            update_attributes["required"] = self.hook_form_item.required

                        update_attributes[
                            self.hook_form_item.validator["validation_trigger"]
                        ] = f"""runValidation({
                            self.hook_form_item.validator.get(
                                "value_to_validate", "$event.target.value"
                            )
                        }, {
                            self.hook_form_item.validator.get(
                                "validation_pattern", "''"
                            )
                        }, {
                            self.hook_form_item.constraints.get(
                                "max_length", "undefined"
                            )
                        }, {
                            self.hook_form_item.constraints.get(
                                "min_length", "undefined"
                            )
                        })"""

                        if isinstance(child, PyInput):
                            if self.hook_form_item.constraints.get("type") == "text":
                                update_attributes["type"] = "text"
                                update_attributes["maxlength"] = (
                                    self.hook_form_item.constraints.get("max_length")
                                )
                                update_attributes["minlength"] = (
                                    self.hook_form_item.constraints.get("min_length")
                                )
                            elif (
                                self.hook_form_item.constraints.get("type") == "number"
                            ):
                                update_attributes["type"] = "number"
                                update_attributes["max"] = (
                                    self.hook_form_item.constraints.get("max")
                                )
                                update_attributes["min"] = (
                                    self.hook_form_item.constraints.get("min")
                                )
                                update_attributes["step"] = (
                                    self.hook_form_item.constraints.get("step")
                                )

                        if isinstance(child, PyTextarea):
                            if self.hook_form_item.constraints.get("type") == "text":
                                update_attributes["maxlength"] = (
                                    self.hook_form_item.constraints.get("max_length")
                                )
                                update_attributes["minlength"] = (
                                    self.hook_form_item.constraints.get("min_length")
                                )

                    combined_attributes = current_attributes | update_attributes
                    child.__init__(**combined_attributes)
                    self.children.append(child)
                else:
                    raise ValueError(
                        f"Invalid child type found. `{self.__class__.__qualname__}` can only have {', '.join([type(allowed_type).__class__.__qualname__ for allowed_type in allowed_child_types])}."
                    )
        else:
            warnings.warn(
                f"Trying to add child to a non-child element: {self.__class__.__qualname__}",
                UserWarning,
                stacklevel=2,
            )
        return self


class FormDescription(P):
    def __init__(self, **attributes: Unpack[PAttributes]):
        base_class_attribute = "text-muted-foreground text-sm"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(class_attribute, base_class_attribute),
            data_slot="form-description",
            **{
                ":id": Statement(
                    content="$id('form-description')", seq_type="assignment"
                )
            },
            **attributes,
        )


class FormMessage(P):
    def __init__(self, **attributes: Unpack[PAttributes]):
        base_class_attribute = "text-destructive text-sm"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(class_attribute, base_class_attribute),
            data_slot="form-message",
            x_show="has_error",
            x_text="error_message",
            **{":id": Statement(content="$id('form-message')", seq_type="assignment")},
            **attributes,
        )

    def __call__(self, *_children: tuple) -> Self:
        warnings.warn(
            f"Trying to add child to a non-child element: {self.__class__.__qualname__}",
            UserWarning,
            stacklevel=2,
        )

        return self
