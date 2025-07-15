"""Base Object for Ingredient, Cookware, and Timing"""

import re
from decimal import Decimal, InvalidOperation

from .const import LONG_TO_SHORT_MAPPINGS, NOTE_PATTERN, QUANTITY_PATTERN, SHORT_TO_LONG_MAPPINGS
from .utils import WholeFraction


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
            self.amount, self.unit = map(str.strip, qstr.split('%'))
        else:
            self.amount = qstr
        self.amount = self.amount.strip()

        # Try storing the quantity as a numeric value
        try:
            if match := re.match(r'(\d+)?\s*(\d+)\s*/\s*(\d+)', self.amount):
                whole, *parts = match.groups()
                whole = int(whole) if whole else 0
                parts = WholeFraction('/'.join(parts))
                self.amount = WholeFraction(whole + parts)
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
        return f'{self:%a %us}'.strip()

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(qstr={repr(self._raw)})'

    def __hash__(self) -> int:
        return hash((self.amount, self.unit))

    def __format__(self, format_spec: str) -> str:
        """
        Return the quantity based on the format spec

        %a - Amount
        %af - Amount as fraction
        %u - Unit
        %ul - Long unit
        %us - short unit
        """
        if not format_spec:
            return str(self)
        s = ''
        fs = iter(format_spec)
        c = next(fs)
        spaces = 0
        while True:
            if c == '%':
                try:
                    c = next(fs)
                except StopIteration:
                    return s
                match c:
                    case 'a':
                        try:
                            c = next(fs)
                        except StopIteration:
                            return s + str(self.amount) if self.amount else ''
                        match c:
                            case 'f':
                                try:
                                    f = WholeFraction(self.amount) if self.amount else ''
                                    s += str(f)
                                    spaces = 0
                                except ValueError:
                                    s += str(self.amount if self.amount else '')
                                    spaces = 0
                            case '%':
                                s += str(self.amount if self.amount else '')
                                spaces = 0
                                continue
                            case _:
                                s += str(self.amount) + c
                                spaces = 0
                    case 'u':
                        try:
                            c = next(fs)
                        except StopIteration:
                            return s + self.unit if self.unit else ''
                        if not self.unit and spaces:
                            s = s[: spaces * -1]
                        match c:
                            case 's':
                                s += LONG_TO_SHORT_MAPPINGS.get(self.unit, self.unit if self.unit else '')
                            case 'l':
                                s += SHORT_TO_LONG_MAPPINGS.get(self.unit, self.unit if self.unit else '')
                            case '%':
                                s += self.unit if self.unit else ''
                                continue
                            case _:
                                s += self.unit if self.unit else '' + c
                    case _:
                        s += f'%{c}'
            else:
                s += c
                if c == ' ':
                    spaces += 1
                else:
                    spaces = 0
            try:
                c = next(fs)
            except StopIteration:
                return s
            continue
        return s


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
