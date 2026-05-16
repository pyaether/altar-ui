"""Form

Build accessible forms with client-side validation.

Composition:
    Use the following composition to build a Form:

    Form
    └── FormField
        ├── FormLabel
        ├── FormDescription
        ├── FormControl
        │   └── ... input / checkbox / textarea / etc.
        └── FormMessage
"""

import json
import warnings
from typing import Literal, Self

from aether.plugins.alpinejs import (
    AlpineHookForm,
    AlpineJSData,
    AlpineValidationTrigger,
    Statement,
    alpine_js_data_merge,
)
from aether.plugins.tailwindcss import tw_merge
from aether.tags.html import (
    Div,
    DivAttributes,
    LabelAttributes,
)
from aether.tags.html import Form as PyForm
from aether.tags.html import FormAttributes as PyFormAttributes
from aether.tags.html import Input as PyInput
from aether.tags.html import Textarea as PyTextarea

from .checkbox import Checkbox
from .field import Field, FieldAlert, FieldDescription, FieldLabel

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack  # noqa: UP035


class Form(PyForm):
    def __init__(self, **attributes: Unpack[PyFormAttributes]):
        base_x_data_attribute = AlpineJSData(
            data={
                "formErrors": {},
                "hasFormErrors": False,
                "setFieldError(id, hasError)": Statement(
                    "{ this.formErrors[id] = hasError; this.hasFormErrors = Object.values(this.formErrors).some(Boolean); }",
                    seq_type="definition",
                ),
                "deleteFieldError(id)": Statement(
                    "{ delete this.formErrors[id]; this.hasFormErrors = Object.values(this.formErrors).some(Boolean); }",
                    seq_type="definition",
                ),
            },
            directive="x-data",
        )
        x_data_attribute = attributes.pop("x_data", None)

        super().__init__(
            x_data=alpine_js_data_merge(base_x_data_attribute, x_data_attribute),
            **attributes,
        )


class FormField(Field):
    def __init__(
        self,
        orientation: Literal["vertical", "horizontal"] | None = "vertical",
        disabled: bool = False,
        **attributes: Unpack[DivAttributes],
    ):
        base_x_data_attribute = AlpineJSData(
            data={
                "has_error": False,
                "is_touched": False,
                "error_message": "",
                "init()": Statement(
                    "{ this.$watch('has_error', value => { if (typeof setFieldError === 'function') setFieldError(this.$id('form-field'), value) }) }",
                    seq_type="definition",
                ),
            },
            directive="x-data",
        )
        x_data_attribute = attributes.pop("x_data", None)

        super().__init__(
            orientation=orientation,
            invalid=None,
            disabled=disabled,
            x_data=alpine_js_data_merge(base_x_data_attribute, x_data_attribute),
            x_id="['form-field', 'field']",
            **{":data-invalid": "has_error && is_touched"},
            **attributes,
        )


class FormLabel(FieldLabel):
    def __init__(self, **attributes: Unpack[LabelAttributes]):
        base_class_attribute = "data-[error=true]:text-destructive"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            **{":data-error": "has_error && is_touched"},
            **attributes,
        )


class FormDescription(FieldDescription):
    pass


class FormControl(Div):
    def __init__(
        self,
        hook_form_item: AlpineHookForm | None = None,
        **attributes: Unpack[DivAttributes],
    ):
        self.hook_form_item = hook_form_item

        base_x_data_attribute = AlpineJSData(
            data={
                "runValidation(value, rules =[], constraints = {}, isRequired = false)": Statement(
                    r"""{
                        const isEmpty = value === undefined || value === null || value === '' || value === false;
                        if (isRequired && isEmpty) {
                            this.has_error = true;
                            this.error_message = "This field is required.";
                            return;
                        }

                        if (!isRequired && isEmpty) {
                            this.has_error = false;
                            this.error_message = "";
                            return;
                        }

                        for (const [type, constraint] of Object.entries(constraints)) {
                            if (type === 'min_length' && value && value.length < constraint.value) {
                                this.has_error = true;
                                this.error_message = constraint.message || `Must be at least ${constraint.value} characters.`;
                                return;
                            }
                            if (type === 'max_length' && value && value.length > constraint.value) {
                                this.has_error = true;
                                this.error_message = constraint.message || `Must be at most ${constraint.value} characters.`;
                                return;
                            }
                        }
                        for (const rule of rules) {
                            if ((rule.test instanceof RegExp && !rule.test.test(value)) || (typeof rule.test === 'function' && !rule.test(value))) {
                                this.has_error = true;
                                this.error_message = rule.message || "Invalid value.";
                                return;
                            }
                        }

                        this.has_error = false;
                        this.error_message = "";
                    }""",
                    seq_type="definition",
                ),
            },
            directive="x-data",
        )
        x_data_attribute = attributes.pop("x_data", None)

        super().__init__(
            x_data=alpine_js_data_merge(base_x_data_attribute, x_data_attribute),
            **attributes,
        )

    def __call__(self, *children: tuple) -> Self:
        if len(children) != 1:
            raise ValueError(
                f"`{self.__class__.__qualname__}` must be called with exactly one child."
            )

        child = children[0]

        allowed_child_types = (Checkbox, PyInput, PyTextarea)
        if not isinstance(child, allowed_child_types):
            raise ValueError(
                f"Invalid child type. Accepted: {', '.join(child_type.__name__ for child_type in allowed_child_types)}."
            )

        current_attributes = {}

        if isinstance(child, (Checkbox,)):
            if forwarded_attributes := getattr(child, "forwarded_attributes", None):
                current_attributes.update(forwarded_attributes)
            if forwarded_class_attribute := getattr(
                child, "forwarded_class_attribute", None
            ):
                current_attributes["_class"] = forwarded_class_attribute
        else:
            current_attributes = dict(child.attributes)

        update_attributes = {}

        update_attributes[":id"] = "fieldId"
        update_attributes[":aria-describedby"] = (
            "(has_error && is_touched) ? `${descriptionId} ${alertId}` : descriptionId"
        )
        update_attributes[":aria-invalid"] = "has_error && is_touched"

        if self.hook_form_item is not None:
            hook_form_item = self.hook_form_item

            if hook_form_item.name is not None:
                update_attributes["name"] = hook_form_item.name

            is_required = "true" if hook_form_item.required else "false"
            if hook_form_item.required is not None:
                update_attributes["required"] = hook_form_item.required

            rules_for_validation = []
            for rule in hook_form_item.validator.get("validation_rules", []):
                test_value = rule.get("test", "''")

                message_raw = rule.get("message")
                message = json.dumps(message_raw) if message_raw else "null"

                rules_for_validation.append(
                    f"{{ test: {test_value}, message: {message} }}"
                )

            rules_for_validation_serialized = f"[{', '.join(rules_for_validation)}]"

            constraints_for_validation = []
            for c_type, constraint in hook_form_item.constraints.items():
                value_raw = constraint.get("value", "")
                value = json.dumps(value_raw)

                message_raw = constraint.get("message")
                message = json.dumps(message_raw) if message_raw else "null"

                constraints_for_validation.append(
                    f"'{c_type}': {{ value: {value}, message: {message} }}"
                )

            constraints_for_validation_serialized = (
                f"{{ {', '.join(constraints_for_validation)} }}"
            )

            trigger = hook_form_item.validator.get(
                "validation_trigger", AlpineValidationTrigger.ON_BLUR
            )
            value_target = hook_form_item.validator.get(
                "value_to_validate", "$event.target.value"
            )

            update_attributes[trigger] = (
                f"is_touched = true; runValidation({value_target}, {rules_for_validation_serialized}, {constraints_for_validation_serialized}, {is_required})"
            )

            init_value = (
                value_target
                if value_target != "$event.target.value"
                else "$el.type === 'checkbox' ? $el.checked : $el.value"
            )
            init_statement = f"runValidation({init_value}, {rules_for_validation_serialized}, {constraints_for_validation_serialized}, {is_required})"

            if "x-init" in current_attributes:
                update_attributes["x-init"] = (
                    f"{current_attributes['x-init']}; $nextTick(() => {{ {init_statement} }})"
                )
            elif "x_init" in current_attributes:
                update_attributes["x_init"] = (
                    f"{current_attributes['x_init']}; $nextTick(() => {{ {init_statement} }})"
                )
            else:
                update_attributes["x-init"] = f"$nextTick(() => {{ {init_statement} }})"

            if isinstance(child, (PyInput, PyTextarea)):
                c_type = hook_form_item.constraints.get("type", {}).get("value")

                if c_type == "text":
                    if "max_length" in hook_form_item.constraints:
                        update_attributes["maxlength"] = hook_form_item.constraints[
                            "max_length"
                        ]["value"]
                    if "min_length" in hook_form_item.constraints:
                        update_attributes["minlength"] = hook_form_item.constraints[
                            "min_length"
                        ]["value"]

                elif c_type == "number" and isinstance(child, PyInput):
                    update_attributes["type"] = "number"
                    for key in ["max", "min", "step"]:
                        if key in hook_form_item.constraints:
                            update_attributes[key] = hook_form_item.constraints[key][
                                "value"
                            ]

        combined_attributes = current_attributes | update_attributes

        grandchildren = None
        if child.have_children and child.children:
            grandchildren = child.children.copy()

        child.__init__(**combined_attributes)

        if grandchildren:
            child.children = grandchildren

        self.children.append(child)

        return self


class FormMessage(FieldAlert):
    def __init__(self, **attributes: Unpack[DivAttributes]):
        super().__init__(
            x_show="has_error && is_touched",
            x_cloak=True,
            x_text="error_message",
            **attributes,
        )

    def __call__(self, *children: tuple) -> Self:
        warnings.warn(
            f"Trying to add child to a non-child element: {self.__class__.__qualname__}",
            UserWarning,
            stacklevel=2,
        )
        return self
