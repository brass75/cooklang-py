import re
from os import PathLike

import frontmatter

from .base_objects import PREFIXES, Cookware, Ingredient
from .const import METADATA_DISPLAY_MAP, METADATA_MAPPINGS


class Metadata:
    """Recipe Metadata Class"""

    def __init__(self, metadata: str):
        self._parsed = frontmatter.Frontmatter().read(metadata)
        if not (attributes := self._parsed.get('attributes')):
            self._mapped = dict()
            return
        if isinstance(attributes, str):
            attrs = dict()
            for line in attributes.splitlines():
                if ':' not in line:
                    continue
                key, value = line.split(':', 1)
                attrs[key.strip()] = value
            attributes = attrs
        self._parsed = {k.strip(): v for k, v in attributes.items()}
        self._mapped = {METADATA_MAPPINGS.get(k.lower(), k.lower()): v for k, v in self._parsed.items()}
        for attr, value in self._mapped.items():
            setattr(self, attr, value)

        for attr, value in self._parsed.items():
            setattr(self, attr, value)

    def __str__(self):
        s = ''
        for k, v in self._mapped.items():
            s += f'{METADATA_DISPLAY_MAP.get(k, k).capitalize()}: {v}\n'
        if s:
            return s + ('-' * 50) + '\n'
        return s


class Recipe:
    def __init__(self, recipe: str):
        self._raw = recipe
        self.metadata = Metadata('')
        if match := re.search(r'(---.*---\s*)(.*)', recipe, re.DOTALL):
            self.metadata = Metadata(match.group(1))
            body = match.group(2)
        else:
            body = recipe
        if not body:
            raise ValueError('No body found in recipe!')
        self.steps = list()
        self.ingredients = list()
        self.cookware = list()
        for line in re.split(r'\n{2,}', body):
            line = re.sub(r'\s+', ' ', line)
            if step := Step(line):
                self.steps.append(step)
                self.ingredients.extend(step.ingredients)
                self.cookware.extend(step.cookware)

    def __iter__(self):
        yield from self.steps

    def __len__(self):
        return len(self.steps)

    def __str__(self):
        s = str(self.metadata)
        s += 'Ingredients:\n\n'
        s += '\n'.join(ing.long_str for ing in self.ingredients)
        s += '\n' + ('-' * 50) + '\n'
        if self.cookware:
            s += '\nCookware:\n\n'
            s += '\n'.join(ing.long_str for ing in self.cookware)
            s += '\n' + ('-' * 50) + '\n'
        s += '\n'
        s += '\n'.join(map(str, self))
        return s.replace('\\', '') + '\n'

    @staticmethod
    def from_file(filename: PathLike):
        """
        Load a recipe from a file

        :param filename: Path like object indicating the location of the file.
        :return: Recipe object
        """
        with open(filename) as f:
            return Recipe(f.read())


class Step:
    def __init__(self, line: str):
        self._raw = line
        self.ingredients = list()
        self.cookware = list()
        self._sections = list()
        self.parse(line)

    def __iter__(self):
        yield from self._sections

    def __len__(self):
        return len(self._sections)

    def __repr__(self):
        return repr(self._sections)

    def parse(self, line: str):
        """
        Parse a line into its component parts
        :param line:
        :return:
        """
        if not (section := self._remove_comments(line)):
            return
        self._sections.clear()
        while match := re.search(r'(?<!\\)[@#~][\S]', section):
            if section[: match.start()].strip():
                self._sections.append(section[: match.start()])
            section = section[match.start() :]
            obj = PREFIXES[section[0]].factory(section)
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
        return re.sub(r'--.*(?:$|\n)|\[-.*?-]', '', line)
