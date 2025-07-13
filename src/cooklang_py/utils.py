"""Utility classes and functions"""

from fractions import Fraction


class WholeFraction(Fraction):
    def __str__(self):
        x = abs(self.numerator) // self.denominator
        return f'{"-" if self < 0 else ""}{f"{x} " if x else ""}{abs(self) - x}'
