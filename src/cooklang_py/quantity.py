import re
from decimal import Decimal, InvalidOperation
from fractions import Fraction
from typing import Any, Self, override

from .const import LONG_TO_SHORT_MAPPINGS, SHORT_TO_LONG_MAPPINGS
from .utils import WholeFraction


class Quantity:
    """Quantity Class"""

    def __init__(self, qstr: str):
        """
        Constructor for the Quantity class

        :param qstr: The quantity string
        """
        self._raw: str = qstr
        self.unit: str = ''
        self.amount: str | Decimal | int | WholeFraction

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

    @override
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Quantity):
            return False
        return self.amount == other.amount and self.unit == other.unit

    @override
    def __str__(self) -> str:
        return f'{self:%a %us}'.strip()

    @override
    def __repr__(self) -> str:
        raw = str(self.amount)
        if self.unit:
            raw += f'%{self.unit}'
        return f'{self.__class__.__name__}(qstr={repr(raw)})'

    @override
    def __hash__(self) -> int:
        return hash((self.amount, self.unit))  # pragma: no cover

    @override
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

        def expand_format_specifier(match: re.Match[str]) -> str:
            spaces = match.group(1)
            placeholder = match.group(2)

            if placeholder.startswith('u') and not self.unit:
                spaces = ''

            if placeholder == 'af':
                try:
                    f = WholeFraction(self.amount) if self.amount else ''
                    return spaces + str(f)
                except ValueError:
                    return spaces + str(self.amount if self.amount else '')
            if placeholder == 'a':
                return spaces + str(self.amount) if self.amount else ''
            if placeholder == 'ul':
                return spaces + SHORT_TO_LONG_MAPPINGS.get(self.unit, self.unit if self.unit else '')
            if placeholder == 'us':
                return spaces + LONG_TO_SHORT_MAPPINGS.get(self.unit, self.unit if self.unit else '')
            if placeholder == 'u':
                return spaces + self.unit if self.unit else ''

            return match.group(0)  # pragma: no cover

        return re.sub(r'(\s*)%(af|a|ul|us|u)', expand_format_specifier, format_spec)

    def __radd__(self, other: Any) -> str:
        if not isinstance(other, str):
            raise TypeError(f'Cannot add {self} to {other.__class__.__name__}')
        return f'{other}{self}'

    def __add__(self, other: Any) -> Self:
        """
        Quantity addition

        Adds either 2 quantities of the same unit or a numeric to a quantity
        :param other: The value to add to the Quantity
        :returns: Quantity
        :raises: ValueError if `other` is a Quantity with a different unit or numeric is < 0
        :raises: TypeError if `other` is not numeric or Quantity
        """
        match other:
            case int() | float() | Decimal():
                if other < 0:
                    raise ValueError(f'Invalid value [{other}] - must be greater than zero.')
                q: Self = eval(repr(self))
                match self.amount:
                    case Fraction():
                        q.amount = WholeFraction(q.amount + other)
                    case Decimal():
                        q.amount += Decimal(other)
                    case _:
                        q.amount += other
                return q
            case Fraction():
                if other < 0:
                    raise ValueError(f'Invalid value [{other}] - must be greater than zero.')
                q: Self = eval(repr(self))
                if isinstance(self.amount, Decimal):
                    q.amount = self.amount + Decimal(other.numerator / other.denominator)
                    return q
                q.amount += other
                return q
            case self.__class__():
                if self.unit != other.unit:
                    raise ValueError(f"Can't add quantity with type {other.unit} to quantity with type {self.unit}")
                return self + other.amount
            case _:
                raise TypeError(f'Unable to add object of type {type(other)} to {self.__class__.__name__}')

    def __mul__(self, other: Any) -> Self:
        """
        Quantity multiplication

        Multiplies a numeric with a quantity
        :param other: The value to add to the Quantity
        :returns: Quantity
        :raises: ValueError if `other` is a Quantity with a different unit or numeric is < 0
        :raises: TypeError if `other` is not numeric or Quantity
        """
        match other:
            case int() | float() | Fraction():
                if other <= 0:
                    raise ValueError(f'Invalid value [{other}] - must be greater than zero.')
                q = eval(repr(self))
                q.amount *= other
                return q
            case _:
                raise TypeError(f'Multiplication of {self.__class__.__name__} cannot be performed with {type(other)}')

    def __truediv__(self, other: Any) -> Self:
        """
        Quantity division

        Divides a numeric with a quantity
        :param other: The value to add to the Quantity
        :returns: Quantity
        :raises: ValueError if `other` is a Quantity with a different unit or numeric is < 0
        :raises: TypeError if `other` is not numeric or Quantity
        """
        match other:
            case int() | float() | Fraction():
                if other <= 0:
                    raise ValueError(f'Invalid value [{other}] - must be greater than zero.')
                q = eval(repr(self))
                q.amount /= other
                return q
            case _:
                raise TypeError(f'Division of {self.__class__.__name__} cannot be performed with {type(other)}')
