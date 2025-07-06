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
