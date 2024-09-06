from typing import Any, Dict

from pytempl.plugins.tailwindcss import tw_merge
from pytempl.tags import Textarea as PyTextarea


class Textarea(PyTextarea):
    def __init__(self, **attributes: Dict[str, Any]):
        base_class_attribute = "flex min-h-[60px] w-full rounded-md border border-input bg-transparent px-3 py-2 text-sm shadow-sm placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50"
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=tw_merge(class_attribute, base_class_attribute), **attributes
        )
