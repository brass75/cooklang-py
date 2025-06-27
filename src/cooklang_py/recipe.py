import re
from os import PathLike

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
        self.cookware = list()
        for line in re.split(r'\n{2,}', body):
            line = re.sub(r'\s+', ' ', line)
            section = Section(line)
            self.sections.append(section)
            self.ingredients.extend(section.ingredients)
            self.cookware.extend(section.cookware)

    def __str__(self):
        s = "Ingredients: \n\n"
        s += '\n'.join(ing.long_str for ing in self.ingredients)
        s += '\n' + ('-' * 50) + '\n'
        if self.cookware:
            s += "\nCookware: \n\n"
            s += '\n'.join(ing.long_str for ing in self.cookware)
            s += '\n' + ('-' * 50) + '\n'
        s += '\n'
        s += '\n'.join(map(str, self.sections))
        return s + '\n'

    @staticmethod
    def from_file(filename: PathLike):
        """
        Load a recipe from a file

        :param filename: Path like object indicating the location of the file.
        :return: Recipe object
        """
        with open(filename) as f:
            return Recipe(f.read())

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
        s = ''
        for section in map(str, self._sections):
            if not any(section.startswith(p) for p in ',;.'):
                s += ' '
            s += section
        return s
