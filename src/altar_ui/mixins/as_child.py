from collections.abc import Generator

from aether import BaseWebElement
from aether.base import _render_element
from aether.plugins.alpinejs import alpine_js_data_merge
from aether.plugins.tailwindcss import tw_merge


class AsChildMixin:
    def __call__(self, *children, allowed_child_types=None):
        if not self.as_child:
            return super().__call__(*children)

        if allowed_child_types is None:
            allowed_child_types = (BaseWebElement,)

        if len(children) != 1:
            raise ValueError(
                f"`{self.__class__.__qualname__}` must be called with exactly one child when `as_child=True`."
            )

        child = children[0]

        if not isinstance(child, allowed_child_types):
            allowed_names = ", ".join([cls.__qualname__ for cls in allowed_child_types])
            raise ValueError(f"Invalid child type. Can only wrap {allowed_names}.")

        current_attributes = child.attributes.copy()
        passthrough_attributes = self.attributes.copy()

        p_class = passthrough_attributes.pop(
            "_class", passthrough_attributes.pop("class", "")
        )
        c_class = current_attributes.pop("_class", current_attributes.pop("class", ""))
        merged_class = tw_merge(p_class, c_class)

        p_x_data = passthrough_attributes.pop(
            "x_data", passthrough_attributes.pop("x-data", None)
        )
        c_x_data = current_attributes.pop(
            "x_data", current_attributes.pop("x-data", None)
        )
        merged_x_data = (
            alpine_js_data_merge(p_x_data, c_x_data) if (p_x_data or c_x_data) else None
        )

        p_x_init = passthrough_attributes.pop(
            "x_init", passthrough_attributes.pop("x-init", None)
        )
        c_x_init = current_attributes.pop(
            "x_init", current_attributes.pop("x-init", None)
        )
        merged_x_init = (
            alpine_js_data_merge(p_x_init, c_x_init) if (p_x_init or c_x_init) else None
        )

        p_style = str(passthrough_attributes.pop("style", "")).strip("; ")
        c_style = str(current_attributes.pop("style", "")).strip("; ")
        merged_style = f"{p_style}; {c_style}".strip("; ")

        merged_events = {}
        for key in list(passthrough_attributes.keys()):
            if (
                key.startswith("@") or key.startswith("x-on:")
            ) and key in current_attributes:
                p_event = str(passthrough_attributes.pop(key)).strip(" ;").strip(";")
                c_event = str(current_attributes.pop(key)).strip(" ;")
                merged_events[key] = f"{p_event}; {c_event}"

        combined_attributes = (
            passthrough_attributes | current_attributes | merged_events
        )

        if merged_class:
            combined_attributes["class"] = merged_class
        if merged_x_data is not None:
            combined_attributes["x-data"] = merged_x_data
        if merged_x_init is not None:
            combined_attributes["x-init"] = merged_x_init
        if merged_style:
            combined_attributes["style"] = merged_style

        child.attributes = combined_attributes
        self.children.append(child)

        return self

    def render(self, stringify: bool = True) -> Generator[str]:
        if not self.as_child:
            yield from super().render(stringify=stringify)
        else:
            for child in self.children:
                yield from _render_element(child, stringify, self.escape_quote)
