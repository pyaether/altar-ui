import warnings
from typing import Any, Dict, Generator, Iterable, Self, Tuple

from pytempl import BaseWebElement, html_class_merge
from pytempl.tags import A, Li, Nav, Ul


class NavigationMenu(Nav):
    def __init__(self, enable_mobile_view: bool = False, **attributes: Dict[str, Any]):
        base_class_attribute = "relative z-10 flex max-w-max flex-1 items-center"
        class_attribute = attributes.pop("_class", "")

        if enable_mobile_view:
            super().__init__(
                _class=html_class_merge(class_attribute, base_class_attribute),
                x_data="{ mobileMenuIsOpen: false }",
                **{"@click.away": "mobileMenuIsOpen = false"},
                **attributes,
            )
        else:
            super().__init__(
                _class=html_class_merge(class_attribute, base_class_attribute),
                **attributes,
            )


class NavigationMenuList(Ul):
    def __init__(self, selected_value: str, **attributes: Dict[str, Any]):
        base_class_attribute = (
            "group flex flex-1 list-none items-center justify-center space-x-1"
        )
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            _class=html_class_merge(class_attribute, base_class_attribute),
            x_data=f"{{ selectedNavItem: '{selected_value}' }}",
            **attributes,
        )

    def __call__(self, *children: Tuple) -> Self:
        for child in children:
            if (
                isinstance(child, str)
                or isinstance(child, BaseWebElement)
                or not isinstance(child, Iterable)
            ):
                if isinstance(child, BaseWebElement):
                    # Check if child has 'value' parameter. If not, warn the user.
                    nav_value = child.attributes.pop("value", None)
                    if not nav_value:
                        warnings.warn(
                            f"Trying to add child that doesn't have 'value' parameter: {self.__class__.__name__}",
                            UserWarning,
                            stacklevel=2,
                        )
                self.children.append(child)
            elif isinstance(child, Generator):
                self.children.extend(list(child))
            elif isinstance(child, type(None)):
                continue
            else:
                self.children.extend(child)

        return self


class NavigationMenuItem(Li):
    def __init__(
        self, value: str, disabled: bool = False, **attributes: Dict[str, Any]
    ):
        self.value = value

        base_class_attribute = "group inline-flex h-9 w-max items-center justify-center rounded-md bg-background px-4 py-2 text-sm font-medium transition-colors hover:bg-accent hover:text-accent-foreground focus:bg-accent focus:text-accent-foreground focus:outline-none"
        class_attribute = attributes.pop("_class", "")
        disabled_class_attribute = "pointer-events-none opacity-50" if disabled else ""

        super().__init__(
            _class=html_class_merge(
                class_attribute, f"{base_class_attribute} {disabled_class_attribute}"
            ),
            value=value,
            **{
                ":class": f"selectedNavItem === '{value}' ? '' : 'text-muted-foreground'",
                ":aria-current": f"selectedNavItem === '{value}' && 'page'",
            },
            **attributes,
        )

    def __call__(self, *children: Tuple) -> Self:
        for child in children:
            if (
                isinstance(child, str)
                or isinstance(child, BaseWebElement)
                or not isinstance(child, Iterable)
            ):
                if isinstance(child, BaseWebElement):
                    # Check if child has 'value' parameter. If not, set it to the parent's value.
                    nav_value = child.attributes.pop("value", None)
                    if not nav_value:
                        child.attributes["@click"] = f"selectedNavItem = '{self.value}'"
                    else:
                        if nav_value != self.value:
                            warnings.warn(
                                "Trying to add child that doesn't have the same 'value' parameter as parent",
                                UserWarning,
                                stacklevel=2,
                            )
                        else:
                            child.attributes["@click"] = (
                                f"selectedNavItem = '{nav_value}'"
                            )
                self.children.append(child)
            elif isinstance(child, Generator):
                self.children.extend(list(child))
            elif isinstance(child, type(None)):
                continue
            else:
                self.children.extend(child)

        return self


class NavigationMenuLink(A):
    def __init__(self, href: str, **attributes: Dict[str, Any]):
        class_attribute = attributes.pop("_class", "")

        super().__init__(
            href=href,
            _class=class_attribute,
            **attributes,
        )
