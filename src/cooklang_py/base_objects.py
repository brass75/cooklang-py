"""Base Object for Ingredient, Cookware, and Timing"""

import re
from typing import Any, Literal, override

from .const import NOTE_PATTERN, QUANTITY_PATTERN
from .quantity import Quantity


class BaseObj:
    """Base Object for Ingredient, Cookware, and Timing"""

    prefix: str = ''
    supports_notes: bool = True

    def __init__(
        self,
        raw: str,
        name: str,
        *,
        quantity: str | None = None,
        notes: str | None = None,
    ):
        """
        Constructor for the BaseObj class

        :param raw: The raw string the ingredient came from
        :param name: The name of the ingredient
        :param quantity: The quantity as described in the raw string
        :param notes: Notes from the raw string
        """
        self.raw: str = raw
        self.name: str = name.strip()
        self._quantity: str | None = quantity.strip() if quantity and quantity.strip() else None
        self.notes: str | None = notes
        self._parsed_quantity: Quantity | Literal[''] = Quantity(self._quantity) if self._quantity else ''

    @override
    def __eq__(self, other: Any) -> bool:
        if not (isinstance(other, BaseObj)):
            return False
        return all(getattr(self, attr) == getattr(other, attr) for attr in ('name', '_parsed_quantity', 'notes'))

    @override
    def __repr__(self) -> str:
        s = f'{self.__class__.__name__}(raw={self.raw!r}, name={self.name!r}, quantity={self._quantity!r}'
        if self.__class__.supports_notes:
            s += f', notes={repr(self.notes)}'
        return s + ')'

    @property
    def quantity(self) -> Quantity | str:
        return self._parsed_quantity

    @override
    def __str__(self) -> str:
        """Short version of the formatted string"""
        if self.quantity:
            return f'{self.name} ({self.quantity})'.strip()
        return self.name

    @override
    def __hash__(self) -> int:
        return hash(tuple(getattr(self, attr) for attr in ('name', '_parsed_quantity', 'notes')))  # pragma: no cover

    @override
    def __format__(self, format_spec: str) -> str:
        """
        Format the string

        %n - Name
        %q - Quantity
        %q[<format>] - Quantity as format
        %c - Notes
        """
        if not format_spec:
            return str(self)

        def expand_format_specifier(match: re.Match[str]) -> str:
            char, spec = match.groups()
            if char == 'c':
                return self.notes if self.notes else ''
            if char == 'n':
                return self.name
            if char == 'q':
                if not spec or not self.quantity:
                    return str(self.quantity)
                return format(self.quantity, spec)
            return match.group(0)  # pragma: no cover

        return re.sub(r'%([cnq])(?:(?<=[q])\[([^]]*)(?:]|$))?', expand_format_specifier, format_spec)

    @classmethod
    def factory(cls, raw: str):
        """
        Factory to create an object

        :param raw: raw string to create from
        :return: An object of cls
        """
        if not cls.prefix:
            raise NotImplementedError(f'{cls.__name__} does not have a prefix set!')
        if not raw.startswith(cls.prefix):
            raise ValueError(f'Raw string does not start with {repr(cls.prefix)}: [{repr(raw[0])}]')
        raw = raw[1:]
        if next_object_starts := [raw.index(prefix) for prefix in PREFIXES if prefix in raw]:
            next_start = min(next_object_starts)
            raw = raw[:next_start]
        note_pattern = NOTE_PATTERN if cls.supports_notes else ''
        if match := re.search(rf'(?P<name>.*?){QUANTITY_PATTERN}{note_pattern}', raw):
            return cls(f'{cls.prefix}{raw[: match.end(match.lastgroup) + 1]}', **match.groupdict())
        note_pattern = note_pattern.removesuffix(
            '?'
        )  # Remove the ? from the end of the pattern to facilitate mathing with note.
        if note_pattern and (match := re.search(rf'^(?P<name>.*?){note_pattern}', raw)):
            return cls(f'{cls.prefix}{raw[: match.end(match.lastgroup) + 1]}', **match.groupdict())
        name = raw.split()[0]
        name = re.sub(r'\W+\Z', '', name) or name
        return cls(f'{cls.prefix}{name}', name=name)

    def __radd__(self, other: Any) -> str:
        if not isinstance(other, str):
            raise TypeError(f'Cannot add {self} to {other.__class__.__name__}')
        return f'{other}{self}'


class Ingredient(BaseObj):
    """Ingredient"""

    prefix: str = '@'
    supports_notes: bool = True


class Cookware(BaseObj):
    """Cookware"""

    prefix: str = '#'
    supports_notes: bool = True


class Timing(BaseObj):
    """Timing"""

    prefix: str = '~'
    supports_notes: bool = False

    @override
    def __str__(self) -> str:
        return f'{self.name.strip()} {str(self.quantity).strip()}'

    @property
    def long_str(self) -> str:
        return str(self)


PREFIXES: dict[str, type[BaseObj]] = {cls.prefix: cls for cls in [Ingredient, Timing, Cookware]}
