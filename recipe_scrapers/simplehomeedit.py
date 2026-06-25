from ._abstract import AbstractScraper
from ._exceptions import ElementNotFoundInHtml


class SimpleHomeEdit(AbstractScraper):
    @classmethod
    def host(cls):
        return "simplehomeedit.com"

    def _clean_ingredient_text(self, li):
        # Remove the checkbox container - this site's theme renders the
        # "▢" checkbox glyph as real screen-reader text content (most WPRM
        # themes do this via CSS ::before instead, which never shows up in
        # get_text()), so it has to be stripped explicitly here.
        checkbox = li.select_one("span.wprm-checkbox-container")
        if checkbox:
            checkbox.extract()

        return li.get_text(" ", strip=True)

    def ingredients(self):
        ingredients = []
        for li in self.soup.select(
            "div.wprm-recipe-ingredients-container li.wprm-recipe-ingredient"
        ):
            text = self._clean_ingredient_text(li)
            if text:
                ingredients.append(text)

        if not ingredients:
            raise ElementNotFoundInHtml("Could not find ingredients.")

        return ingredients

    def instructions(self):
        instructions = []
        for li in self.soup.select(
            "div.wprm-recipe-instructions-container li.wprm-recipe-instruction"
        ):
            text = li.get_text(" ", strip=True)
            if text:
                instructions.append(text)

        if not instructions:
            raise ElementNotFoundInHtml("Could not find instructions.")

        return "\n".join(instructions)