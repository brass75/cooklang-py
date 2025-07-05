import pytest

from cooklang_py import Recipe


@pytest.mark.parametrize(
    'recipe',
    [
        'potato_kugel',
        'no_md',
    ],
)
def test_recipe(recipe):
    expected = open(f'tests/data/{recipe}.txt').read()
    recipe = Recipe.from_file(f'tests/data/{recipe}.md')
    assert str(recipe) == expected
