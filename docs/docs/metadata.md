## The `Metadata` Class

The Cooklang specification includes `frontmatter` metadata at the top of the recipe. This class
contains that metadata. The metadata is available via `.` notation (`md.tags`), index notation
(`md['tags']`), and a `get` method (`md.get('tags', '')`).

For Cooklang's [canonical metadata](https://cooklang.org/docs/spec/#canonical-metadata)
items will be stored both as they appear in the recipe as well as converted to a canonical
name as defined by `METADATA_MAPPINGS`. For your convenience there is also a mapping for display
purposes called `METADATA_DISPLAY_MAP`. Both of these mappings can be imported:

```python
from cooklang_py.const import METADATA_DISPLAY_MAP, METADATA_MAPPINGS
```
