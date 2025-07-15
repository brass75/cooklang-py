## The `Ingredient` Class


The `Ingredient` class defines the ingredients needed to prepare a recipe. An example Cooklang
ingredient string would be `@cheddar cheese{1%cup}(shredded)` which would be represented like:

```python
ingredient = Ingredient.factory('@cheddar cheese{1%cup}(shredded)')
repr(ingredient)
"Ingredient(raw='@cheddar cheese{1%cup}(shredded)', name='cheddar cheese', quantity='1%cup', notes='shredded')"
print(ingredient)
cheddar cheese (1 cup)
print(ingredient.long_str)
1 cup cheddar cheese (shredded)
```

### Attributes, properties, and methods

`Ingredient` does not implement any unique attributes, properties, or methods. It inherits
all from [`BaseObj`](base_object.md/#attributes-properties-and-methods)

### Class definition

The `Ingredient` class is defined as follows:

```python
class Ingredient(BaseObj):
    """Ingredient"""

    prefix = '@'
    supports_notes = True
```

#### Dunder implementations

`__str__` - The string will be formatted `<name> (<quantity>)`. This is the equivaluent to using the 
`%n (%q)` `format_spec`.

`__format__` - String Formatting.
The following options are available for format_spec:

- %n - Name
- %q - Quantity
- %q[<format>] - Quantity as format
- %c - Notes

Examples:

```python
from cooklang_py import Ingredient
ing = Ingredient(raw='', name='flour', quantity='1 3/4%cup', notes='sifted')
print(format(ing, '%n (%q[%af %ul])'))
flour (1 3/4 cup)
print(format(ing, '%q %n (%c)'))
1 3/4 c flour (sifted)
print(format(ing, '%n (%q)'))
flour (1 3/4 c)

```

