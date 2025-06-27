""" Base Object for Ingredient, Cookware, and Timing """
import re

from cooklang_py.const import QUANTITY_PATTERN, NOTE_PATTERN, UNIT_MAPPINGS


class Quantity:
    """ Quantity Class """

    def __init__(self, qstr: str):
        self._raw = qstr
        self.unit = ''
        if '%' in qstr:
            self.amount, self.unit = qstr.split('%')
        else:
            self.amount = qstr

    def __str__(self):
        return f'{self.amount} {UNIT_MAPPINGS.get(self.unit, self.unit)}'.strip()

    def __repr__(self):
        return f'{self.__class__.__name__}(qstr={repr(self._raw)})'

class BaseObj:
    """ Base Object for Ingredient, Cookware, and Timing """
    prefix = None
    supports_notes = True

    def __init__(self, raw: str, name: str, *, quantity: str = None, notes: str = None, ):
        """
        Constructor for the BaseObj class

        :param raw: The raw string the ingredient came from
        :param name: The name of the ingredient
        :param quantity: The quantity as described in the raw string
        :param notes: Notes from the raw string
        """
        self.raw = raw
        self.name = name.strip()
        self._quantity = quantity
        self.notes = notes
        self._parsed_quantity = Quantity(quantity) if quantity else ''

    @property
    def long_str(self) -> str:
        """ Formatted string """
        s = str(self.quantity) + ' ' if self.quantity else ''
        s = f'{s}{self.name}'
        if self.notes:
            s += f' ({self.notes})'
        return s.strip()

    def __repr__(self):
        params = [f'quantity={repr(self._quantity)}']
        if self.__class__.supports_notes:
            params.append(f'notes={repr(self.notes)}')

    @property
    def quantity(self) -> str:
        return self._parsed_quantity

    def __str__(self):
        """ Short version of the formatted string """
        if self.quantity:
            return f'{self.name} ({self.quantity})'.strip()
        return self.name

    def __hash__(self):
        return hash(self.raw)

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
            return cls(f'{cls.prefix}{raw[:match.end(match.lastgroup) + 1]}', **match.groupdict())
        if note_pattern and (match := re.search(rf'^(P<name>[\S]+){note_pattern}', raw)):
            return cls(f'{cls.prefix}{raw[:match.end(match.lastgroup) + 1]}', **match.groupdict())
        name = raw.split()[0]
        return cls(f'{cls.prefix}{name}', name=name)

class Ingredient(BaseObj):
    """ Ingredient """
    prefix = '@'
    supports_notes = True

class Cookware(BaseObj):
    """ Ingredient """
    prefix = '#'
    supports_notes = True

class Timing(BaseObj):
    """ Ingredient """
    prefix = '~'
    supports_notes = False

    def __str__(self):
        return str(self.quantity).strip()

    def long_str(self) -> str:
        return str(self)


PREFIXES = {
    '@': Ingredient,
    '#': Cookware,
    '~': Timing,
}

