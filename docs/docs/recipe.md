## The `Recipe` Class

The `Recipe` class brings everything together and is the heart of cooklang-py. It will parse a recipe from a
Cooklang string into its component [metadata](metadata.md) and [`Step`s ](step.md).

### Attributes, properties, and methods

The `Recipe` class defines the following methods:

```python
Recipe(recipe: str, prefixes: dict = PREFIXES)
    """
    Parse the recipe string into a Recipe object.

    :param recipe: Recipe string
    :param prefixes: Prefixes for parsing. Default is PREFIXES constant.
                     This allows for overriding the handling of one or
                     more of the base objects.
    """
```

- `recipe` - this is the Cooklang string containing the recipe (metadata and steps)
- `prefixes` - allows for overriding the implementations of `Ingredient`, `Cookware`,
and `Timing` classes.

```python
@staticmethod
from_file(filename: PathLike, prefixes: dict = PREFIXES) -> Recipe
```

The `from_file` method will create a `Recipe` from a file containing a Cooklang recipe.

- `filename` - the full path to a Cooklang recipe file.
- `prefixes` - allows for overriding the implementations of `Ingredient`, `Cookware`,
and `Timing` classes.

**NOTE** Any class being used to override one of the [`BaseObj`](base_object.md) must inherit
from `BaseObj` or implement the `factory` class method and the `long_str` property.

The `Recipe` class exposes the following attributes:

- `ingredients` - A list of all ingredients used by the recipe. Note that this list is in the order in which
ingredients appear in the recipe and may contain duplicates.
- `cookware` - A list of all equipment used by the recipe. Note that this list is in the order in which
cookware appear in the recipe and may contain duplicates.
- `steps` - The individual parsed lines from the recipe.
- `metadata` - The metadata from the recipe.


#### Dunder implementations

The `Recipe` class implements the following dunder methods:

- `__iter__` - This will iterate over the `Steps` attribute
- `__len__` - This is the number of steps
