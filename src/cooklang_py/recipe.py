import re

import frontmatter

from .base_objects import Ingredient, Cookware, PREFIXES


class Recipe:
    def __init__(self, recipe: str):
        self._raw = recipe
        self._parsed = frontmatter.Frontmatter().read(recipe)
        if not (body := self._parsed['body']):
            raise ValueError('No body found in recipe!')
        self.sections = list()
        self.ingredients = list()
        for line in re.split(r'\n{2,}', body):
            line = re.sub(r'\s+', ' ', line)
            section = Section(line)
            self.sections.append(section)
            self.ingredients.extend(section.ingredients)

    def __str__(self):
        s = '\n'.join(ing.long_str for ing in self.ingredients)
        s += '\n\n' + ('-' * 50) + '\n\n'
        s += '\n'.join(map(str, self.sections))
        return s + '\n'

class Section:
    def __init__(self, line: str):
        self._raw = line
        self.ingredients = list()
        self.cookware = list()
        self._sections = list()
        self.parse(line)

    def parse(self, line: str):
        """
        Parse a line into its component parts
        :param line:
        :return:
        """
        section = line
        self._sections.clear()
        while match := re.search(r'(?<!\\)[@#~]', section):
            self._sections.append(section[:match.start()].strip())
            section = section[match.start():]
            obj = PREFIXES[section[0]].factory(section)
            self._sections.append(obj)
            section = section.removeprefix(obj.raw)
            match obj:
                case Ingredient():
                    self.ingredients.append(obj)
                case Cookware():
                    self.cookware.append(obj)
        if section := section.strip():
            self._sections.append(section)

    def __str__(self):
        return ' '.join(map(str, self._sections))
