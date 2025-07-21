from fractions import Fraction

import pytest

from cooklang_py import Quantity


def test_quantity_string_addition():
    """Test string addition"""
    assert 'Testing: ' + Quantity('1%cup') == 'Testing: 1 c'


def test_quantity_quantity_addition():
    """Test quantity addition"""
    with pytest.raises(TypeError):
        Quantity('1%cup') + [1, 2]


@pytest.mark.parametrize('input_string, expected', [('1 3/4%cup', '1 3/4 c')])
def test_quantity_string_no_format(input_string, expected):
    """Test Quantity as str with no formatting"""
    quant = Quantity(input_string)
    assert str(quant) == expected


@pytest.mark.parametrize(
    'input_str, format_string, expected',
    [
        (
            '1 3/4%cup',
            ('%af %ul', '%a %ul', '%af %us', '%a %us', '%b%c%d', '%u%a'),
            ('1 3/4 cup', '1 3/4 cup', '1 3/4 c', '1 3/4 c', '%b%c%d', 'cup1 3/4'),
        ),
        (
            '1.75%cup',
            ('%af %ul', '%a %ul', '%af %us', '%a %us', '%b%c%d', '%u%a'),
            ('1 3/4 cup', '1.75 cup', '1 3/4 c', '1.75 c', '%b%c%d', 'cup1.75'),
        ),
        (
            '1 3/4%c',
            ('%af %ul', '%a %ul', '%af %us', '%a %us', '%b%c%d', '%u%a'),
            ('1 3/4 cups', '1 3/4 cups', '1 3/4 c', '1 3/4 c', '%b%c%d', 'c1 3/4'),
        ),
        (
            '1.75%c',
            ('%af %ul', '%a %ul', '%af %us', '%a %us', '%b%c%d', '%u%a'),
            ('1 3/4 cups', '1.75 cups', '1 3/4 c', '1.75 c', '%b%c%d', 'c1.75'),
        ),
    ],
)
def test_formating(input_str, format_string, expected):
    """Test formatting"""
    for fstring, expected in zip(format_string, expected):
        assert f'{Quantity(input_str):{fstring}}' == expected, f'{fstring} != {expected}'


@pytest.mark.parametrize(
    'quantity, other, expected',
    [
        (Quantity('1 1/2%cup'), Fraction(3, 2), 3),
        (Quantity('1 1/2%cup'), 1.5, 3),
        (Quantity('1 1/2%cup'), 1, Fraction(5, 2)),
        (Quantity('1.5%cup'), Fraction(3, 2), 3),
        (Quantity('1.5%cup'), 1.5, 3),
        (Quantity('1.5%cup'), 1, Fraction(5, 2)),
        (Quantity('1.5%cup'), Quantity('1.5%cup'), 3),
    ],
)
def test_quantity_addition(quantity, other, expected):
    assert (quantity + other).amount == expected


def test_quantity_quantity_addition_different_units():
    with pytest.raises(ValueError):
        Quantity('1.5%cup') + Quantity('1.5%tbsp')


def test_quantity_quantity_addition_invalid_amount():
    with pytest.raises(ValueError):
        Quantity('1.5%cup') + (-1)


@pytest.mark.parametrize(
    'quantity, other, expected',
    [
        (Quantity('1 1/2%cup'), 2, 3),
        (Quantity('1 1/2%cup'), 1.5, 2.25),
        (Quantity('1 1/2%cup'), Fraction(3, 2), 2.25),
    ],
)
def test_quantity_multiplication(quantity, other, expected):
    assert (quantity * other).amount == expected


def test_quantity_multiplication_invalid_amount():
    with pytest.raises(ValueError):
        Quantity('1 1/2%cup') * (-1)


def test_quantity_multiplication_invalid_operand():
    with pytest.raises(TypeError):
        Quantity('1 1/2%cup') * Quantity('1 1/2%cup')


@pytest.mark.parametrize(
    'quantity, other, expected',
    [
        (Quantity('3%cup'), 2, 1.5),
        (Quantity('3%cup'), 1.5, 2),
        (Quantity('3%cup'), Fraction(3, 2), 2),
    ],
)
def test_quantity_division(quantity, other, expected):
    assert (quantity / other).amount == expected


def test_quantity_division_invalid_amount():
    with pytest.raises(ValueError):
        Quantity('1 1/2%cup') / (-1)


def test_quantity_division_invalid_operand():
    with pytest.raises(TypeError):
        Quantity('1 1/2%cup') / Quantity('1 1/2%cup')
