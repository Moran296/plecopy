from collections import namedtuple
import unicodedata
import re

Card = namedtuple("Card", "headword pronunciation definition")

def print_with_hebrew(text, *args, **kwargs):
    if type(text) == str and len(text) > 0:
        if 'HEBREW' in unicodedata.name(text.strip()[0]):
            text = "".join(text[-1::-1])

    print(text, *args, **kwargs)

class PlecoPy:
    def __init__(self):
        self.categories = {}

    def create_category(self, line):
        path = line[2:].strip()
        path = path.split("/")
        father_category = self.categories
        for name in path:
            if name not in father_category:
                father_category[name] = {}
            father_category = father_category[name]

        return father_category

    def parse_card(self, line):
        card = Card(*line.strip().split("\t"))
        return card._replace(definition=list(card.definition.split("; ")))

    def present_card(self, card, only_short_def=True):
        print (f"{card.headword}  {card.pronunciation}")
        for definition in card.definition:
            if only_short_def and len(definition.split()) > 3:
                continue
            print_with_hebrew (f"{definition}")

    def present_category(self, category, only_short_def=True):
        if type(category) != dict:
            return
        for key, value in category.items():
            if key == 'cards':
                for card in category[key]:
                    self.present_card(card, only_short_def)
                    print('\n')
            else:
                print_with_hebrew(f"{key}")
                self.present_category(value, only_short_def)

    def present_all(self, only_short_def=True):
        self.present_category(self.categories, only_short_def)

    def parse_txt_file(self, path):
        """Parse a text file into a list of cards."""
        lines = []
        with open(path, "r", encoding="utf-8-sig") as f:
            lines = f.readlines()

        category = None
        prefix = '//'
        if not lines[0].startswith(prefix):
            print ("first line: " + lines[0])
            raise ValueError("First line must be a category (starts with //)")

        for line in lines:
            if line.startswith(prefix):
                category = self.create_category(line)
                category['cards'] = []
                continue
            try:
                card = self.parse_card(line)
            except:
                #print ("Error parsing line: " + line)
                continue

            category['cards'].append(card)

p = PlecoPy()
p.parse_txt_file('pleco_tayarut.txt')
p.present_all(only_short_def=False)