"""Constants"""

QUANTITY_PATTERN = r'(?<!\\){(?P<quantity>.*?)}'
NOTE_PATTERN = r'(?:\((?P<notes>.*)\))?'

LONG_TO_SHORT_MAPPINGS = {
    'teaspoon': 'tsp',
    'tablespoon': 'tbsp',
    'teaspoons': 'tsp',
    'tablespoons': 'tbsp',
    'cup': 'c',
    'cups': 'c',
    'quarts': 'qt',
    'gallons': 'gal',
    'quart': 'qt',
    'gallon': 'gal',
    'kilo': 'kg',
    'gram': 'g',
    'ounce': 'oz',
    'pound': 'lb',
    'liter': 'l',
    'milliliter': 'ml',
    'kilos': 'kg',
    'grams': 'g',
    'ounces': 'oz',
    'pounds': 'lb',
    'liters': 'l',
    'milliliters': 'ml',
    'hour': 'h',
    'hours': 'h',
    'minute': 'm',
    'minutes': 'm',
    'second': 's',
    'seconds': 's',
}

SHORT_TO_LONG_MAPPINGS = {v: k for k, v in LONG_TO_SHORT_MAPPINGS.items()}

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
