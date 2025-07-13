import pytest

from cooklang_py import WholeFraction


@pytest.mark.parametrize(
    'input_string, expected',
    [
        ('7/4', '1 3/4'),
        ('-7/4', '-1 3/4'),
        ('-3/4', '-3/4'),
        ('-1.5', '-1 1/2'),
        ('1.75', '1 3/4'),
        ('-.5', '-1/2'),
    ],
)
def test_whole_fraction(input_string, expected):
    """Test fraction to string works as expected"""
    assert str(WholeFraction(input_string)) == expected
