import re
from collections.abc import Generator
from os import PathLike
from typing import Any

import frontmatter

from .base_objects import PREFIXES, BaseObj, Cookware, Ingredient
from .const import METADATA_DISPLAY_MAP, METADATA_MAPPINGS


class Metadata:
    """Recipe Metadata Class"""

    def __init__(self, metadata: dict):
        """
        Initialize the Metadata class

        :param metadata: Dictionary of metadata
        """
        self._parsed = {k.strip(): v for k, v in metadata.items()}
        self._mapped = {METADATA_MAPPINGS.get(k.lower(), k.lower()): v for k, v in self._parsed.items()}
        for attr, value in self._mapped.items():
            setattr(self, attr, value)

        for attr, value in self._parsed.items():
            setattr(self, attr, value)

    def __str__(self) -> str:
        s = ''
        for k, v in self._mapped.items():
            s += f'{METADATA_DISPLAY_MAP.get(k, k).capitalize()}: {v}\n'
        if s:
            return s + ('-' * 50) + '\n'
        return s

    def __getitem__(self, key: str) -> Any:
        if key in self._parsed:
            return self._parsed[key]
        if key in self._mapped:
            return self._mapped[key]
        raise KeyError(f'Unable to find {key=}.')

    def get(self, key: str, default: Any = None) -> Any:
        """
        Attempt to get the value associated with key

        :param key: The key to get
        :param default: Default value to return if the key is not found
        :return: The entry at key or default
        """
        try:
            return self[key]
        except KeyError:
            return default


class Recipe:
    def __init__(self, recipe: str, prefixes: dict = PREFIXES):
        """
        Parse the recipe string into a Recipe object.

        :param recipe: Recipe string
        :param prefixes: Prefixes for parsing. Default is PREFIXES constant.
                         This allows for overriding the handling of one or
                         more of the base objects.
        """
        self._raw = recipe
        metadata, body = frontmatter.parse(re.sub(r':(?=\S)', ': ', recipe))
        self.metadata = Metadata(metadata)
        if not body:
            raise ValueError('No body found in recipe!')
        self.steps = list()
        self.ingredients = list()
        self.cookware = list()
        for line in re.split(r'\n{2,}', body):
            line = re.sub(r'\s+', ' ', line)
            if step := Step(line, prefixes):
                self.steps.append(step)
                self.ingredients.extend(step.ingredients)
                self.cookware.extend(step.cookware)

    def __iter__(self) -> Generator:
        yield from self.steps

    def __len__(self) -> int:
        return len(self.steps)

    def __str__(self) -> str:
        s = str(self.metadata)
        s += 'Ingredients:\n\n'
        s += '\n'.join(
            (f'{ing:%q[%af %us] %n (%c)}' if ing.notes else f'{ing:%q[%af %us] %n}') for ing in self.ingredients
        )
        s += '\n' + ('-' * 50) + '\n'
        if self.cookware:
            s += '\nCookware:\n\n'
            s += '\n'.join(
                (f'{cw:%q[%af %us] %n (%c)}' if cw.notes else f'{cw:%q[%af %us] %n}') for cw in self.cookware
            )
            s += '\n' + ('-' * 50) + '\n'
        s += '\n'
        s += '\n'.join(map(str, self))
        return s.replace('\\', '') + '\n'

    @staticmethod
    def from_file(filename: PathLike, prefixes: dict = PREFIXES):
        """
        Load a recipe from a file

        :param filename: Path like object indicating the location of the file.
        :param prefixes: Prefixes for parsing. Default is PREFIXES constant.
                         This allows for overriding the handling of one or
                         more of the base objects.
        :return: Recipe object
        """
        with open(filename) as f:
            return Recipe(f.read(), prefixes)


class Step:
    def __init__(self, line: str, prefixes: dict = PREFIXES):
        """
        Parse a line into its sections and objects

        :param line: The line to parse
        :param prefixes: Prefixes for parsing. Default is PREFIXES constant.
                 This allows for overriding the handling of one or
                 more of the base objects.

        """
        self._raw: str = line
        self.ingredients: list[Ingredient] = list()
        self.cookware: list[Cookware] = list()
        self._sections: list[str | BaseObj] = list()
        self._prefixes: dict[str, type[BaseObj]] = prefixes
        self._parse(line)

    def __iter__(self):
        yield from self._sections

    def __len__(self):
        return len(self._sections)

    def __repr__(self):
        return repr(self._sections)

    def _parse(self, line: str):
        """
        Parse a line into its component parts

        :param line: The line to parse
        """
        if not (section := self._remove_comments(line)):
            return
        self._sections.clear()
        while match := re.search(r'(?<!\\)[@#~][\S]', section):
            if section[: match.start()].strip():
                self._sections.append(section[: match.start()])
            section = section[match.start() :]
            obj = self._prefixes[section[0]].factory(section)
            self._sections.append(obj)
            section = section.removeprefix(obj.raw)
            match obj:
                case Ingredient():
                    self.ingredients.append(obj)
                case Cookware():
                    self.cookware.append(obj)
        if section.strip():
            self._sections.append(section)

    def __str__(self):
        return ''.join(map(str, self)).rstrip()

    @staticmethod
    def _remove_comments(line: str) -> str:
        """
        Remove comments from the line.

        :param line: The line to clean of comments
        :return: The line without comments.
        """
        return re.sub(r'--.*(?:$|\n)|\[-.*?-]', '', line)
