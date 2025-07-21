"""Test for base objects"""

import pytest

from cooklang_py import Ingredient


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


def test_baseobj_string_addition():
    """Test string addition"""
    assert 'Testing: ' + Ingredient('', name='flour', quantity='1%cup') == 'Testing: flour (1 c)'


def test_baseobj_baseobj_addition():
    """Test quantity addition"""
    with pytest.raises(TypeError):
        Ingredient('', name='flour', quantity='1%cup') + Ingredient('', name='flour', quantity='1%cup')
