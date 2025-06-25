""" Constants """

QUANTITY_PATTERN = r'(?<!\\){(?P<quantity>.*?)}'
NOTE_PATTERN = r'(?:\((?P<notes>.*)\))?'

UNIT_MAPPINGS = {
    'teaspoon': 'tsp',
    'tablespoon': 'tbsp',
    'quart': 'qt',
    'gallon': 'gal',
    'kilo': 'kg',
    'gram': 'g',
    'ounce': 'oz',
    'pound': 'lb',
    'liter': 'l',
    'milliliter': 'ml',
}

