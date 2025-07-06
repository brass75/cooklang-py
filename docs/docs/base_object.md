## The `BaseObj` Class

The `BaseObj` class serves as the base for these objects:

- `Ingredient`
- `Timing`
- `Cookware`

and defines certain methods, attributes, and properties that are common to all. Each base object
must define the following:

- `prefix` - This is the character, defined in the Cooklang specification, that denotes whether
the text following is an ingredient (`@`), timing (`~`), or cookware (`#`).
- `supports_notes` - This is a boolean value indicating whether the defined object allows for notes
per the Cooklang specification. Currently only `timing` does not support notes.

### Attributes, properties, and methods

The `BaseObj` class contains the following methods:

```python
BaseObj(
    raw: str,
    name: str,
    *,
    quantity: str = None,
    notes: str = None,
):
    """
    Constructor for the BaseObj class

    :param raw: The raw string the ingredient came from
    :param name: The name of the ingredient
    :param quantity: The quantity as described in the raw string
    :param notes: Notes from the raw string
    """
```

Parameters for the `BaseObj` method:

- `raw` - the raw string that was used to create the `BaseObj`. If the `BaseObj` is being
created directly this can be `''` with no ill effects.
- `name`  - the name of the object
- `quantity` - the quantity required as a string in the format `<amount>%<unit>`. Optional.
- `notes` - string defining preparation notes. Optional.


```python
@classmethod
factory(raw)
```
The `factory` method for `BaseObj` will parse the `raw` string provided and create a new
`BaseObj`

```python
# In this example we are using the factory to create an Ingredient.

Ingredient.factory('@cheddar cheese{1%cup}(shredded)')
Ingredient(raw='@cheddar cheese{1%cup}(shredded)', name='cheddar cheese', quantity='1%cup', notes='shredded')
```

The `BaseObj` class contains the following attributes:

- `name` - the name of the object
- `notes` - preparation notes
- `raw` - the raw string used to create the ingredient. (Note that the `BaseObj` doesn't
actually parse the string unless created with the `factory` method. The raw string may or
may not be passed by the instantiating code.)

The `BaseObj` class contains the following properties:

- `quantity` - The `Quantity` of the ingredient. If the `Ingredient` does not have a `Quantity`
this will be `''`.
- `long_str` - This returns the `BaseObj` as a string in the format `<quantity> <name> (<notes>)`.
This is in contrast to `str(BaseObj)` which returns `<name> (<quantity>)`.
