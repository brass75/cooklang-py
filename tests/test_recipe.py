from pathlib import Path

import pytest

from cooklang_py import Cookware, Ingredient, Recipe, Step, Timing


@pytest.fixture
def step():
    yield Step(
        'Stir in the @potatoes{3%cups}(drained and grated), '
        'turn into a greased #baking dish{1.5%qt}, '
        'and bake until browned, approximately ~{1%hour}.'
    )


@pytest.mark.parametrize(
    'recipe',
    [
        'potato_kugel',
        'no_md',
    ],
)
def test_recipe(recipe):
    expected = open(f'tests/data/{recipe}.txt').read()
    recipe = Recipe.from_file(Path(f'tests/data/{recipe}.md'))
    assert str(recipe) == expected


@pytest.mark.parametrize(
    'format_options, expected',
    [
        (
            '',
            'Stir in the potatoes (3 c), turn into a greased baking dish (1.5 qt), and bake until '
            'browned, approximately  1 h.',
        ),
        (
            '%n (%q[%af %ul])',
            'Stir in the potatoes (3 cups), turn into a greased baking dish (1 1/2 quart), and bake until '
            'browned, approximately  (1 hour).',
        ),
        (
            {Cookware: '%c %n (%q[%af %u])', Ingredient: '%c %n (%q[%af %ul])', Timing: '%q[%af %ul]'},
            'Stir in the drained and grated potatoes (3 cups), turn into a greased  baking dish (1 1/2 qt), and bake '
            'until browned, approximately 1 hour.',
        ),
        (
            {'Cookware': '%c %n (%q[%af %u])', 'Ingredient': '%c %n (%q[%af %ul])'},
            'Stir in the drained and grated potatoes (3 cups), turn into a greased  baking dish (1 1/2 qt), and bake '
            'until browned, approximately  1 h.',
        ),
    ],
)
def test_step_formatted_string(step, format_options, expected):
    """Tests string formatting"""
    actual = step.formatted_string(format_options)
    assert actual == expected


def test_step_formatted_string_error(step):
    """Test that unrecognized key raises error"""
    with pytest.raises(ValueError):
        step.formatted_string({'unknown': ''})
