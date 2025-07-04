import re

import pytest
import yaml
from yaml import BaseLoader

from cooklang_py import Cookware, Ingredient, Recipe, Step, Timing

CANONICAL_TESTS = yaml.load(open('tests/data/canonical.yaml', 'rb').read().decode('utf-8'), BaseLoader)


def get_args(test_dict: dict) -> dict:
    res = dict()
    amount = test_dict.get('quantity')
    unit = test_dict.get('units')
    res['name'] = test_dict.get('name')
    if unit and amount:
        res['quantity'] = f'{amount}%{unit}'
    elif amount:
        res['quantity'] = amount
    return res


@pytest.mark.parametrize('name, data', CANONICAL_TESTS['tests'].items())
def test_canonical_cases(name, data):
    """Run the canonical test cases"""
    if data['result'].get('metadata'):
        return handle_metadata_test(name, data)
    test_input = data['source']
    all_expected = iter(data['result']['steps'])
    for line in test_input.split('\n\n'):
        actual = Step(line)
        if not len(actual):
            assert len(data['result']['steps']) == 0
            continue
        expected = next(all_expected)
        assert len(expected) == len(actual), f'{name} failed! {line=}'
        actual = iter(actual)
        for i, e_step in enumerate(expected):
            a_step = next(actual)
            match e_step['type']:
                case 'text':
                    assert str(a_step).strip() == e_step['value'].strip(), f'{name} failed! {line=}'
                case 'ingredient':
                    ingredient = Ingredient(raw=line, **get_args(e_step))
                    assert a_step == ingredient, f'{name} failed! {line=}'
                case 'cookware':
                    cookware = Cookware(raw=line, **get_args(e_step))
                    assert a_step == cookware, f'{name} failed! {line=}'
                case 'timer':
                    timing = Timing(raw=line, **get_args(e_step))
                    assert a_step == timing, f'{name} failed! {line=}'
    return None


def handle_metadata_test(name, data):
    """Metadata tests"""
    test_input = re.sub(r'\s*>>\s*', '\n', data['source']).strip()
    metadata = Recipe(f'---\n{test_input}\n---\n123\n').metadata
    result = data['result']['metadata']
    for attr, value in result.items():
        parsed = getattr(metadata, attr, None)
        assert parsed == value, f'Incorrect attribute: {attr} -- {parsed} != {value}'
