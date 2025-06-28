# cooklang-py

A parser for the [Cooklang recipe markup language](https://cooklang.org)

## Installation

To install just run:

```shell
pip install cooklang-py
```

## `Recipe`

The `Recipe` is the primary unit. There are 2 ways to create a `Recipe` object:

```python
from cooklang_py import Recipe

# Create from a string in memory
recipe_string = '<your recipe here>'
recipe = Recipe(recipe_string)

# Create from a file
recipe_file = '/path/to/recipe/file'
recipe = Recipe.from_file(recipe_file)
```

Just like a recipe in a book a `Recipe` contains:

- Ingredients
- Cookware / equipment
- Timings
- Metadata (servings, cook time, etc.)

To see how to define these in your input please refer to the
[Cooklang language specification](https://cooklang.org/docs/spec/#comments)

When the recipe is parsed there will be a list of `Step` objects. Each step object can contain:

- Ingredients
- Cookware
- Timings
- Instructions (text)

At both the `Recipe` and `Step` level you can access the list of `Ingredients` and `Cookware`
for the recipe or step.

### Cookware, Timings, and Ingredients

Cookware, timings, and ingredients are the backbone of the recipe. In this package all three
inherit from the `BaseObj`. They all have the following 3 attributes:

- `name` - the name of the item (i.e. pot, carrot, etc.)
- `quantity` - how much is needed
  - For `Ingredient` quantity defaults to "some" if it is not set.
  - For `Cookware` quantity defaults to 1 if it is not set.
- `notes` - any notes for the item (i.e. "greased", "peeled and diced", etc.)
  - `Timings` do not have notes per the Cooklang specification.

## Compatibility

`cooklang-py` passes all canonical tests defined at
[https://github.com/cooklang/cooklang-rs/blob/main/tests/canonical.yaml](https://github.com/cooklang/cooklang-rs/blob/main/tests/canonical.yaml)
for the following platforms:

- Linux
- MacOS
- Windows (with the exception of test cases with Unicode characters.)
