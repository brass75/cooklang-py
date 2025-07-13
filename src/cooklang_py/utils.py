"""Utility classes and functions"""

from fractions import Fraction


class WholeFraction(Fraction):
    def __str__(self):
        whole = abs(self.numerator) // self.denominator
        part = abs(self) - whole
        sign = '-' if self < 0 else ''
        if whole and part:
            return f'{sign}{whole} {part}'
        if whole:
            return f'{sign}{whole}'
        if part:
            return f'{sign}{part}'
        return '0'
