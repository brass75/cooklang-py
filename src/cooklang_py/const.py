"""Constants"""

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
