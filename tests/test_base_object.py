"""Test for base objects"""

import pytest

from cooklang_py import Ingredient, Quantity


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
    'fmt_spec, expected',
    [
        ('', 'flour (1.75 c)'),
        ('%q[%a %ul] %n (%c)', '1.75 cup flour (level)'),
        ('%n %q[%af %us] (%c)', 'flour 1 3/4 c (level)'),
        ('%n %q[%af %us', 'flour 1 3/4 c'),
    ],
)
def test_formatting(fmt_spec, expected):
    """Test formatting"""
    ing = Ingredient(raw='@flour{1.75%cup}(level)', name='flour', quantity='1.75%cup', notes='level')
    assert f'{ing:{fmt_spec}}' == expected


def test_formatting_no_unit():
    """Test formatting with name, amount,  and comment"""
    ing = Ingredient(raw='@eggs{3}(beaten)', name='eggs', quantity='3', notes='beaten')
    assert f'{ing:%q[%af %us] %n (%c)}' == '3 eggs (beaten)'


def test_formatting_no_unit_or_notes():
    """Test formatting with name and amount"""
    ing = Ingredient(raw='@eggs{3}', name='eggs', quantity='3')
    assert f'{ing:%q[%af %us] %n (%c)}' == '3 eggs ()'

def test_quantity_string_addition():
    """Test string addition"""
    assert 'Testing: ' + Quantity('1%cup') == 'Testing: 1 c'

def test_quantity_quantity_addition():
    """Test quantity addition"""
    with pytest.raises(TypeError):
        Quantity('1%cup') + Quantity('1%cup')

def test_baseobj_string_addition():
    """Test string addition"""
    assert 'Testing: ' + Ingredient('', name='flour', quantity='1%cup') == 'Testing: flour (1 c)'

def test_baseobj_baseobj_addition():
    """Test quantity addition"""
    with pytest.raises(TypeError):
        Ingredient('', name='flour', quantity='1%cup') + Ingredient('', name='flour', quantity='1%cup')
