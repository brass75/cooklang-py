"""Base Object for Ingredient, Cookware, and Timing"""

import re
from decimal import Decimal, InvalidOperation
from fractions import Fraction

from .const import NOTE_PATTERN, QUANTITY_PATTERN, UNIT_MAPPINGS


class Quantity:
    """Quantity Class"""

    def __init__(self, qstr: str):
        """
        Constructor for the Quantity class

        :param qstr: The quantity string
        """
        self._raw = qstr
        self.unit = ''
        if '%' in qstr:
            self.amount, self.unit = qstr.split('%')
            self.unit = self.unit.strip()
        else:
            self.amount = qstr
        self.amount = self.amount.strip()

        # Try storing the quantity as a numeric value
        try:
            if '/' in self.amount:
                self.amount = Fraction(re.sub(r'\s+', '', self.amount))
            elif '.' in self.amount:
                self.amount = Decimal(self.amount)
            else:
                self.amount = int(self.amount)
        except (ValueError, InvalidOperation):
            pass

    def __eq__(self, other) -> bool:
        if not isinstance(other, Quantity):
            return False
        return self.amount == other.amount and self.unit == other.unit

    def __str__(self) -> str:
        return f'{self.amount} {UNIT_MAPPINGS.get(self.unit, self.unit)}'.strip()

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(qstr={repr(self._raw)})'

    def __hash__(self) -> int:
        return hash((self.amount, self.unit))


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

    @property
    def long_str(self) -> str:
        """Formatted string"""
        s = str(self.quantity) + ' ' if self.quantity else ''
        s = f'{s}{self.name}'
        if self.notes:
            s += f' ({self.notes})'
        return s.strip()

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
