## The `Timing` Class

The `Timing` class defines the timing aspect of a recipe. An example Cooklang timing string
would be `~bake{1%hour}` which would be represented like:

```python
timing = Timing.factory('~bake{1%hour}')
print(timing)
bake 1 h
repr(timing)
"Timing(raw='~bake{1%hour}', name='bake', quantity='1%hour')"
```

### Attributes, properties, and methods

`Timing` does not implement any unique attributes, properties, or methods. It inherits
all from [`BaseObj`](base_object.md/#attributes-properties-and-methods)

### Overrides

Since `Tming` does not support `notes` it overrides both the `__str__` and `long_str` of `BaseObj`
to be:

```python
    def __str__(self) -> str:
        return f'{self.name.strip()} {str(self.quantity).strip()}'
```

### Class definition

The `Timing` class is defined as follows:

```python
class Timing(BaseObj):
    """Timing"""

    prefix = '~'
    supports_notes = False
```
