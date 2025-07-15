## The `Cookware` Class

The `Cookware` class defines the equipment needed to prepare a recipe. An example Cooklang
cookware string would be `#pot{1}(with lid)` which would be represented like:

```python
cookware = Cookware.factory('#pot{1}(with lid)')
repr(cookware)
"Cookware(raw='#pot{1}(with lid)', name='pot', quantity='1', notes='with lid')"
print(cookware)
pot (1)
print(cookware.long_str)
1 pot (with lid)
```

### Attributes, properties, and methods

`Cookware` does not implement any unique attributes, properties, or methods. It inherits
all from [`BaseObj`](base_object.md/#attributes-properties-and-methods)

### Class definition

The `Cookware` class is defined as follows:

```python
class Cookware(BaseObj):
    """Ingredient"""

    prefix = '#'
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
from cooklang_py import Cookware
cw = Cookware(raw='', name='pot', quantity='5%quart', notes='with a cover')
print(format(cw, '%n (%q[%af %ul])'))
pot (5 quart)
print(format(cw, '%q %n (%c)'))
5 qt pot (with a cover)
print(format(cw, '%n (%q)'))
pot (5 qt)

```