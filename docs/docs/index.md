## What is cooklang-py

cooklang-py is a Python based parsing library for the [Cooklang](https://cooklang.org)
recipe markup language. It will parse a Cooklang file and give access to:

- Recipe
- Metadata
- [Step](step.md)
- [Ingredients](ingredient.md)
- [Cookware](cookware.md)
- [Timing](timing.md)

Note that `Ingredients`, `Cookware`, and `Timings` all derive from the
[`BaseObj` class](base_object.md).

### Installing cooklang-py

cooklang-py requires Python 3.10 or above. You can download python from [python.org](https://python.org).

- Linux/MacOS: [python.org](https://python.org)
- Windows: [Microsoft Store](https://apps.microsoft.com/store/detail/python-311/9NRWMJP3717K)

cooklang-py is available via PyPI and can be installed via `pip` or `uv`:

```shell
# pip
$ pip install cooklang-py

#uv
$ uv pip install cooklang-py
```
