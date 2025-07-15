## The `Quantity` Class

Cooklang defines the quantity part of an object as being `{<amount>%<unit>}` which can be attached
to any of the base objects (`Ingredient`, `Cookware`, `Timing`.) These base objects will include
a `Quantity` objects when they are so defined.

```python
quantity = Quantity('1%cup')
repr(quantity)
"Quantity(qstr='1%cup')"
print(quantity)
1 cup
quantity.amount
1
quantity.unit
'cup'
```

### Attributes, properties, and methods

The `Qunatity` class has the following methods:

```python
Quantity(qstr: str)
    """
    Constructor for the Quantity class

    :param qstr: The quantity string
    """
```

- `qstr` - The string representing the quantity.

The `Quantity` class exposes the following attributes:

- `unit` - This is the unit that the quantity is in.
- `amount` The amount of the quantity. This will be stored in a numeric form (`Fraction`,
`Decimal`, or `int`) when possible.

#### Dunder implementations

The `Quantity` class implements the following dunder methods:

`__eq__` - Two `Quantity` objects are considered to be equal if the unit and amounts are equal:

```python
Quantity('0.5%cup') == Quantity('1/2%cup')
True
```

`__str__` - The string will be formatted `<amount> <unit>` and the `unit` will be converted to an
abbreviated unit per `UNIT_MAPPINGS` (importable from `cooklang_py.const`). The `str` representaion
is equialent to using the `%a %us` `format_spec` `<amount> <short unit>`

`__format__` - String Formatting.
The following options are available for format_spec:

- %a - Amount
- %af - Amount as fraction
- %u - Unit
- %ul - Long unit
- %us - short unit

Examples:

```python
from cooklang_py import Quantity
q = Quantity('1 3/4%cup')
print(format(q, '%af ul'))
1 3/4 ul
print(format(q, '%af us'))
1 3/4 us
print(format(q, '%af %ul'))
1 3/4 cup
print(format(q, '%af %us'))
1 3/4 c
print(format(q, '%u (%a)'))
cup(1 3/4)
```
