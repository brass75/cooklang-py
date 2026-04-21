from cooklang_py import Cookware

## The `Step` Class

The `Step` class is the workhorse of cooklang-py. It takes a line from a Cooklang recipe and
parses it into its component parts. Those parts can include one or more of:

- Text instructions
- Ingredients
- Cookware
- Timings

If we take the following line from a Cooklang recipe and parse it to a `Step` we get:

```python
step = Step('Beat @eggs{2} for ~{1%minute} and gently pour into a hot #frying pan{} over a medium heat.')
repr(step)
"[
    'Beat ',
    Ingredient(raw='@eggs{2}', name='eggs', quantity='2', notes=None),
    ' for ',
    Timing(raw='~{1%minute}', name='', quantity='1%minute'),
    ' and gently pour into a hot ',
    Cookware(raw='#frying pan{}', name='frying pan', quantity=None, notes=None),
    ' over a medium heat.',
]"
print(step)
Beat eggs (2) for  1 m and gently pour into a hot frying pan over a medium heat.
```

You can see that each part of the line was parsed to the appropriate part. The `Step` object
even contains a list of all of the `Cookware` and `Ingredients` required for the line:

```python
step.ingredients
[Ingredient(raw='@eggs{2}', name='eggs', quantity='2', notes=None)]
step.cookware
[Cookware(raw='#frying pan{}', name='frying pan', quantity=None, notes=None)]
```

### Attributes, properties, and methods

The `Step` class contains the following methods:

```python
Step(line: str, prefixes: dict = PREFIXES):
    """
    Parse a line into its sections and objects

    :param line: The line to parse
    :param prefixes: Prefixes for parsing. Default is PREFIXES constant.
             This allows for overriding the handling of one or
             more of the base objects.
        """
```

This will create a new `Step` object by parsing the `line` parameter into its component sections.
The `prefixes` parameter allows for overriding the implementations of `Ingredient`, `Cookware`,
and `Timing` classes.

**NOTE** Any class being used to override one of the [`BaseObj`](base_object.md) must inherit
from `BaseObj` or implement the `factory` class method and the `long_str` property.

```python
def formatted_string(self, format_options: str | dict[str | type[BaseObj], str] = '') -> str:
"""
Generate a formatted string of the Step object

:param format_options: Either a string containing the format options to pass to all objects,
                       or a dictionary where the key is a BaseObj class or the name of the
                       BaseObj class and the value is the format string to apply
:return: Formatted string representation of the Step object
"""
```

The `formatted_string` method will generate a formatted string from the step. It takes a single
parameter, `format_options`, that is either a format string that will be applied to all `BaseObject`
instances in the `Step` or a dictionary mapping each `BaseObj` type to the desired format string
for that object. This method gives additional flexibility when formatting the output of a `Step` as
compared to calling `str(my_step)`. When the dictionary mapping option is being used it should be:

```python
{
    Ingredient: <format string>,
    Cookware: <format string>,
    Timing: <format string>,
}
```

If using the dictionary mapping the keys can either be the types or the type names as strings. If
there are any unrecognized keys (that do not map to `self.obj_mapping`) a `ValueError` will be raised.

**NOTE** Any additional `BaseObj` subclasses must be added to the `obj_mapping` dictionary to be
to use this functionality.

**NOTE** For the specifications of the format strings please see the documentation for [Ingredient],
[Cookware], and [Timing].

The `Step` class exposes the following attributes:

- `ingredients` - the list of ingredients required for a given step
- `cookware` - the list of equipment required for a given step
- `obj_mapping` - a mapping of lower class object names to their types

#### Dunder implementations

The `Step` class implements the following dunder methods:

- `__iter__` - This will iterate over the parsed sections
- `__len__` - This is the number of parsed sections.

[Ingredient]:ingredient.md
[Cookware]:cookware.md
[Timing]:timing.md
