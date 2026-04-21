from pathlib import Path

import pytest

from cooklang_py import Cookware, Ingredient, Recipe, Step, Timing


@pytest.mark.parametrize(
    'recipe, expected_metadata, length',
    [
        (
            'potato_kugel',
            {
                'category': 'side dish',
                'description': 'Potato Kugel is a traditional Ashkenazi Jewish recipe. It is '
                'often served as a side dish during a Passover Seder. This '
                'recipe is also the base for potato pancakes (latkes), simply '
                'fry small dollops of the potato mix instead of baking.',
                'diet': 'kosher, vegetarian',
                'difficulty': 'easy',
                'locale': 'en_US',
                'servings': '6-8 people',
                'time.cook': '60m',
                'time.prep': '30m',
                'title': 'Potato Kugel',
                'cook time': '60m',
                'course': 'side dish',
                'prep time': '30m',
            },
            5,
        ),
        ('no_md', {}, 1),
    ],
)
def test_recipe(recipe, expected_metadata, length):
    expected = open(f'tests/data/{recipe}.txt').read()
    recipe = Recipe.from_file(Path(f'tests/data/{recipe}.md'))
    assert str(recipe) == expected
    for k, v in expected_metadata.items():
        assert recipe.metadata[k] == v
        assert recipe.metadata.get(k) == v
    with pytest.raises(KeyError):
        recipe.metadata['does not exist']
    assert recipe.metadata.get('does not exist') is None
    assert len(recipe) == length


def test_recipe_no_body():
    with pytest.raises(ValueError):
        Recipe("""---
attr: value
---""")


@pytest.fixture
def step():
    yield Step(
        'Stir in the @potatoes{3%cups}(drained and grated), '
        'turn into a greased #baking dish{1.5%qt}, '
        'and bake until browned, approximately ~{1%hour}.'
    )


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


def test_steps_repr(step):
    assert repr(step) == (
        "['Stir in the ', Ingredient(raw='@potatoes{3%cups}(drained and grated)', "
        "name='potatoes', quantity='3%cups', notes='drained and grated'), ', turn "
        "into a greased ', Cookware(raw='#baking dish{1.5%qt}', name='baking dish', "
        "quantity='1.5%qt', notes=None), ', and bake until browned, approximately ', "
        "Timing(raw='~{1%hour}', name='', quantity='1%hour'), '.']"
    )
