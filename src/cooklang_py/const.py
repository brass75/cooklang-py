"""Constants"""

QUANTITY_PATTERN = r'(?<!\\){(?P<quantity>.*?)}'
NOTE_PATTERN = r'(?:\((?P<notes>.*)\))?'

UNIT_MAPPINGS = {
    'teaspoon': 'tsp',
    'tablespoon': 'tbsp',
    'cup': 'c',
    'cups': 'c',
    'quart': 'qt',
    'gallon': 'gal',
    'kilo': 'kg',
    'gram': 'g',
    'ounce': 'oz',
    'pound': 'lb',
    'liter': 'l',
    'milliliter': 'ml',
    'hour': 'h',
    'minute': 'm',
    'second': 's',
}

REVERSE_UNIT_MAPPING = {v: k for k, v in UNIT_MAPPINGS.items()}

METADATA_MAPPINGS = {
    'source': 'source.name',
    'author': 'source.author',
    'serves': 'servings',
    'yield': 'servings',
    'course': 'category',
    'time required': 'duration',
    'time': 'duration',
    'prep time': 'time.prep',
    'cook time': 'time.cook',
    'image': 'images',
    'picture': 'images',
    'pictures': 'images',
    'introduction': 'description',
}

METADATA_DISPLAY_MAP = {
    'source.name': 'Recipe from',
    'source.author': 'Recipe author',
    'source.url': 'Recipe URL',
    'duration': 'Total cook time',
    'time.prep': 'Prep time',
    'time.cook': 'Cook time',
}
