"""Base Object for Ingredient, Cookware, and Timing"""

import re

from .const import NOTE_PATTERN, QUANTITY_PATTERN
from .quantity import Quantity


class BaseObj:
    """Base Object for Ingredient, Cookware, and Timing"""

    prefix = None
    supports_notes = True

    def __init__(
        self,
        raw: str,
        name: str,
        *,
        quantity: str = None,
        notes: str = None,
    ):
        """
        Constructor for the BaseObj class

        :param raw: The raw string the ingredient came from
        :param name: The name of the ingredient
        :param quantity: The quantity as described in the raw string
        :param notes: Notes from the raw string
        """
        self.raw = raw
        self.name = name.strip()
        self._quantity = quantity.strip() if quantity and quantity.strip() else None
        self.notes = notes
        self._parsed_quantity = Quantity(self._quantity) if self._quantity else ''

    def __eq__(self, other) -> bool:
        if not (isinstance(other, BaseObj)):
            return False
        return all(getattr(self, attr) == getattr(other, attr) for attr in ('name', '_parsed_quantity', 'notes'))

    def __repr__(self) -> str:
        s = f'{self.__class__.__name__}(raw={self.raw!r}, name={self.name!r}, quantity={self._quantity!r}'
        if self.__class__.supports_notes:
            s += f', notes={repr(self.notes)}'
        return s + ')'

    @property
    def quantity(self) -> Quantity | str:
        return self._parsed_quantity

    def __str__(self) -> str:
        """Short version of the formatted string"""
        if self.quantity:
            return f'{self.name} ({self.quantity})'.strip()
        return self.name

    def __hash__(self) -> int:
        return hash(tuple(getattr(self, attr) for attr in ('name', '_parsed_quantity', 'notes')))

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
        s = ''
        fs = iter(format_spec)
        c = next(fs)
        while True:
            if c == '%':
                try:
                    c = next(fs)
                except StopIteration:
                    return s
                match c:
                    case 'c':
                        if self.notes:
                            s += self.notes
                    case 'n':
                        s += self.name
                    case 'q':
                        try:
                            c = next(fs)
                        except StopIteration:
                            return s + str(self.quantity)
                        qformat_spec = ''
                        if c == '[':
                            try:
                                while (c := next(fs)) != ']':
                                    qformat_spec += c
                            except StopIteration:
                                return s + f'{self.quantity:{qformat_spec}}' if self.quantity else ''
                        s += (f'{self.quantity:{qformat_spec}}' if self.quantity else '') + (c if c != ']' else '')
                    case _:
                        s += f'%{c}'
            else:
                s += c
            try:
                c = next(fs)
            except StopIteration:
                return s
            continue
        return s

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
        if note_pattern and (match := re.search(rf'^(P<name>[\S]+){note_pattern}', raw)):
            return cls(f'{cls.prefix}{raw[: match.end(match.lastgroup) + 1]}', **match.groupdict())
        name = raw.split()[0]
        name = re.sub(r'\W+$', '', name) or name
        return cls(f'{cls.prefix}{name}', name=name)

    def __radd__(self, other) -> str:
        if not isinstance(other, str):
            raise TypeError(f'Cannot add {self} to {other.__class__.__name__}')
        return f'{other}{self}'


class Ingredient(BaseObj):
    """Ingredient"""

    prefix = '@'
    supports_notes = True


class Cookware(BaseObj):
    """Cookware"""

    prefix = '#'
    supports_notes = True


class Timing(BaseObj):
    """Timing"""

    prefix = '~'
    supports_notes = False

    def __str__(self) -> str:
        return f'{self.name.strip()} {str(self.quantity).strip()}'

    @property
    def long_str(self) -> str:
        return str(self)


PREFIXES = {
    '@': Ingredient,
    '#': Cookware,
    '~': Timing,
}
