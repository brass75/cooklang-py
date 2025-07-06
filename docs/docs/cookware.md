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
