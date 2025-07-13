"""Test for base objects"""

import pytest

from cooklang_py import Quantity


@pytest.mark.parametrize('input_string, expected', [('1 3/4%cup', '1 3/4 c')])
def test_quantity_string_no_format(input_string, expected):
    """Test Quantity as str with no formatting"""
    quant = Quantity(input_string)
    assert str(quant) == expected


@pytest.mark.parametrize(
    'input_string, expected',
    [
        ('1 3/4%cup', '1 3/4 cup'),
        ('1.75%cup', '1 3/4 cup'),
    ],
)
def test_quantity_string_format_fraction(input_string, expected):
    """Test string output as fraction when using format"""
    assert f'{Quantity(input_string):%af %u}' == expected


@pytest.mark.parametrize(
    'input_string, expected',
    [
        ('1 3/4%cup', '1 3/4 cup'),
        ('1.75%cup', '1.75 cup'),
    ],
)
def test_quantity_string_format_no_change(input_string, expected):
    """Test string output as decimal when using format"""
    assert f'{Quantity(input_string):%a %u}' == expected


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
